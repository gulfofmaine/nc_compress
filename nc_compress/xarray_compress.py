"""
Compress using xarray
"""
from pathlib import Path
import logging

try:
    from dask.diagnostics import ProgressBar
except ImportError:
    ProgressBar = None

import xarray as xr

logger = logging.getLogger("nc_compress")


def compress_encodings(ds: xr.Dataset, level: int = 5, method: str = "zlib") -> xr.Dataset:
    """Add compression encodings to xr.Dataset"""
    compression = {method: True, "complevel": level}

    logger.debug(f"Setting compression to {compression} for {ds.data_vars}")

    for var in ds.data_vars:
        ds[var].encoding.update(compression)

    return ds


def compress(input_path: Path, output_path: Path, level: int = 5, method: str = "zlib"):
    """Load, compress, and write out dataset"""
    logger.info(f"Opening dataset from {input_path}")

    with xr.open_dataset(input_path) as ds:
        ds = compress_encodings(ds, level, method)

        logger.info(f"Saving compressed NetCDF to {output_path}")

        if ProgressBar:
            output = ds.to_netcdf(output_path, compute=False)

            with ProgressBar():
                results = output.compute()

        else:
            logger.debug("ProgressBar is not importable from dask.diagnostics, saving quietly.")
            ds.to_netcdf(output_path)
