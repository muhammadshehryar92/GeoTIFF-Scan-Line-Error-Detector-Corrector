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
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name
