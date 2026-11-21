"""
GeoTIFF Scan-Line Error Detector & Corrector
Detects and interpolates Scan Line Corrector (SLC-off) and missing scan-line
artifacts in GeoTIFF rasters while preserving CRS and spatial metadata.
"""

import argparse
from pathlib import Path
import numpy as np
import rasterio
from scipy.interpolate import griddata


def detect_scanline_mask(band_array: np.ndarray, nodata_val: float = 0) -> np.ndarray:
    """
    Identify missing scan-line pixels in a 2D raster band.

    Parameters
    ----------
    band_array : np.ndarray
        2D array representing a single raster band.
    nodata_val : float, optional
        Pixel value representing missing scan lines (default is 0).

    Returns
    -------
    np.ndarray
        Boolean mask where True indicates corrupted/missing pixels.
    """
    if np.isnan(nodata_val):
        return np.isnan(band_array)
    return (band_array == nodata_val) | np.isnan(band_array)


def interpolate_band(
    band_array: np.ndarray,
    missing_mask: np.ndarray,
    method: str = "linear",
) -> np.ndarray:
    """
    Reconstruct missing scan-line pixels using 2D spatial interpolation.

    Parameters
    ----------
    band_array : np.ndarray
        2D array with missing scan-line gaps.
    missing_mask : np.ndarray
        Boolean array where True indicates pixels to be filled.
    method : str, optional
        Interpolation method: 'linear', 'nearest', or 'cubic' (default 'linear').

    Returns
    -------
    np.ndarray
        Gap-filled 2D raster band array.
    """
    if not np.any(missing_mask):
        return band_array.copy()

    rows, cols = band_array.shape
    grid_y, grid_x = np.mgrid[0:rows, 0:cols]

    valid_mask = ~missing_mask
    if not np.any(valid_mask):
        raise ValueError("Raster band contains no valid pixels for interpolation.")

    valid_points = np.column_stack((grid_y[valid_mask], grid_x[valid_mask]))
    valid_values = band_array[valid_mask]
    missing_points = np.column_stack((grid_y[missing_mask], grid_x[missing_mask]))

    interpolated_values = griddata(
        valid_points,
        valid_values,
        missing_points,
        method=method,
    )

    # Fallback to nearest-neighbor for edge pixels outside convex hull
    nan_edges = np.isnan(interpolated_values)
    if np.any(nan_edges):
        interpolated_values[nan_edges] = griddata(
            valid_points,
            valid_values,
            missing_points[nan_edges],
            method="nearest",
        )

    filled_band = band_array.astype(np.float64).copy()
    filled_band[missing_mask] = interpolated_values
    return filled_band.astype(band_array.dtype)


def repair_geotiff(
    input_path: str,
    output_path: str,
    nodata_val: float | None = None,
    method: str = "linear",
) -> dict:
    """
    Detect and repair scan-line errors across all bands of a GeoTIFF file.

    Parameters
    ----------
    input_path : str
        Path to corrupted input GeoTIFF.
    output_path : str
        Path where repaired GeoTIFF will be written.
    nodata_val : float, optional
        Explicit NoData value. Uses raster metadata NoData or 0 if None.
    method : str, optional
        Spatial interpolation method ('linear', 'nearest', 'cubic').

    Returns
    -------
    dict
        Summary statistics including total pixels and gap percentage per band.
    """
    stats = {"input": str(input_path), "output": str(output_path), "bands": {}}

    with rasterio.open(input_path) as src:
        profile = src.profile.copy()
        target_nodata = (
            nodata_val
            if nodata_val is not None
            else (src.nodata if src.nodata is not None else 0)
        )

        repaired_bands = []
        for band_idx in range(1, src.count + 1):
            band_data = src.read(band_idx)
            mask = detect_scanline_mask(band_data, nodata_val=target_nodata)
            gap_pct = float(np.mean(mask) * 100.0)

            repaired = interpolate_band(band_data, mask, method=method)
            repaired_bands.append(repaired)

            stats["bands"][band_idx] = {
                "missing_pixels": int(np.sum(mask)),
                "gap_percentage": round(gap_pct, 2),
            }

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(output_path, "w", **profile) as dst:
            for band_idx, band_arr in enumerate(repaired_bands, start=1):
                dst.write(band_arr, band_idx)

    return stats


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detect and correct scan-line errors in GeoTIFF files."
    )
    parser.add_argument("input_tif", help="Path to corrupted input GeoTIFF (.tif)")
    parser.add_argument("output_tif", help="Path to save repaired GeoTIFF (.tif)")
    parser.add_argument(
        "--nodata",
        type=float,
        default=None,
        help="NoData/gap pixel value (defaults to raster metadata or 0)",
    )
    parser.add_argument(
        "--method",
        choices=["linear", "nearest", "cubic"],
        default="linear",
        help="Spatial interpolation algorithm (default: linear)",
    )
    args = parser.parse_args()

    summary = repair_geotiff(
        input_path=args.input_tif,
        output_path=args.output_tif,
        nodata_val=args.nodata,
        method=args.method,
    )
    print(f"Successfully repaired GeoTIFF: {summary['output']}")
    for band, info in summary["bands"].items():
        print(
            f"  Band {band}: filled {info['missing_pixels']} pixels "
            f"({info['gap_percentage']}% gap)"
        )


if __name__ == "__main__":
    main()
