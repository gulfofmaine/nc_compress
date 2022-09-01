#!/usr/bin/env python
"""
nc_compress

Take a source NetCDF and compress it.

Optionally it can use xbitinfo to try to smartly discard unused bits
for higher compression with `--method=xbitinfo`.

Example usage:
    nc_compress /path/to/uncompressed.nc /path/to/compressed.nc
"""
import argparse
from pathlib import Path
import sys
import logging
from typing import List, Optional


logger = logging.getLogger("nc_compress")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)


class Arguments(argparse.Namespace):
    """Paths, compression level, and compression_method"""
    input_path: Path
    output_path: Path
    level: int = 5
    method: str = "zlib"
    hide_stats: bool = False


def parse_arguments(args: List[str]) -> Arguments:
    parser = argparse.ArgumentParser(
        # description="Compress NetCDF"
        description=__doc__
    )
    parser.add_argument("input_path", help="Input NetCDF", type=Path)
    parser.add_argument("output_path", help="Output compressed NetCDF", type=Path)

    parser.add_argument("--level", "-l", help="Compression level (default: 5)", type=int, default=5)
    parser.add_argument("--method", "-m", help="Compression method (default: zlib)", type=str, default="zlib")
    parser.add_argument("--hide_stats", help="Hide compression statistics", action="store_true")

    return parser.parse_args(args)



def main(unparsed_args: Optional[List[str]] = None):
    """Run compression from command line"""
    if not unparsed_args:
        unparsed_args = sys.argv[1:]
    args = parse_arguments(unparsed_args)

    input_mb = args.input_path.stat().st_size / 1_000_000

    if args.method in ("xb", "xbit", "xbitinfo"):
        logger.error("Compression with xbitinfo has not been implemented yet")
        sys.exit(1)
    else:
        from nc_compress.xarray_compress import compress

        compress(args.input_path, args.output_path, args.level, args.method)

    output_mb = args.output_path.stat().st_size / 1_000_000

    logger.info(f"Compressed from {input_mb:,.2f} MB to {output_mb:,.2f} MB.")


if __name__ == "__main__":
    main(sys.argv[1:])
