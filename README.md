Here is your updated, copy-paste-ready `README.md` populated with your exact GitHub username (`muhammadshehryar92`) and repository name (`GeoTIFF-Scan-Line-Error-Detector-Corrector`).

```markdown
# GeoTIFF Scan-Line Error Detector & Corrector

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)
![Status: Active Development](https://img.shields.io/badge/status-active%20development-orange.svg)

An open-source, headless Python utility to programmatically detect, mask, and interpolate Scan Line Corrector (SLC-off) errors and missing scan-line artifacts in GeoTIFF rasters while preserving full geospatial metadata.

---

## Overview & Motivation

Historical Earth observation archives—most notably **Landsat 7 ETM+ imagery acquired after May 2003**—suffer from systematic wedge-shaped data gaps caused by the Scan Line Corrector (SLC) hardware failure. While this 2003–2013 archive is critical for long-term climate, drought, and land-cover time-series modeling, repairing these rasters typically requires proprietary desktop GIS software or manual GUI workflows that break automated batch-processing pipelines.

This repository provides a lightweight, scriptable Python workflow designed for remote sensing researchers and analysts working in automated or Linux/CLI environments.

---

## Features

### Current Capabilities
* **Automated Gap Detection:** Identifies missing scan lines and `NoData` / zero-value wedge masks across single-band and multi-band GeoTIFF files.
* **Spatial Gap Interpolation:** Reconstructs missing scan-line pixel values using neighborhood spatial interpolation.
* **Geospatial Metadata Preservation:** Retains original Coordinate Reference Systems (CRS), affine geotransforms, data types, and GeoTIFF tags via `rasterio`.
* **Headless Execution:** Runs purely via Python without desktop GIS dependencies.

### Planned Roadmap
* [ ] Multi-temporal reference-scene compositing (Local Linear Histogram Matching / regression-based filling).
* [ ] Quantitative validation suite (RMSE and SSIM benchmarking using synthetic SLC-off masks).
* [ ] Command-Line Interface (CLI) for batch directory processing.
* [ ] Automated `pytest` suite with sample GeoTIFF test fixtures and PyPI packaging.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/muhammadshehryar92/GeoTIFF-Scan-Line-Error-Detector-Corrector.git](https://github.com/muhammadshehryar92/GeoTIFF-Scan-Line-Error-Detector-Corrector.git)
   cd GeoTIFF-Scan-Line-Error-Detector-Corrector

```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```



---

## Quick Start

```python
import rasterio
import numpy as np
from scipy.interpolate import griddata

# Example workflow using the repository's correction module
from fix_scanline import detect_scanline_mask, repair_geotiff

input_tif = "path/to/corrupted_landsat7_band.tif"
output_tif = "path/to/repaired_landsat7_band.tif"

# Detect missing scan-line mask and interpolate gaps
mask = detect_scanline_mask(input_tif, nodata_val=0)
repair_geotiff(input_tif, output_tif, nodata_val=0, method="linear")

print(f"Repaired GeoTIFF saved to: {output_tif}")

```

---

## Project Structure

```text
GeoTIFF-Scan-Line-Error-Detector-Corrector/
├── fix_scanline.py      # Core scan-line detection and interpolation functions
├── requirements.txt     # Python dependencies (rasterio, numpy, scipy)
├── LICENSE              # MIT License
└── README.md            # Project documentation

```

---

## Contributing

Contributions, bug reports, and test datasets (especially multi-band Landsat 7 ETM+ SLC-off scenes) are welcome. Feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

```

*(Note: Just make sure `fix_scanline.py` in the **Quick Start** and **Project Structure** sections matches the exact `.py` filename inside your repository, and change `rasterio` to `osgeo.gdal` if your script uses GDAL instead of Rasterio.)*

```
