from importlib.metadata import entry_points
from setuptools import setup

pkg_name = "nc_compress"

setup(
    use_scm_version={
        "write_to": f"{pkg_name}/_version.py",
        "write_to_template": '__version__ = "{version}"',
        "tag_regex": r"^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$",
    },
    entry_points={
        "console_scripts": [
            "nc_compress = nc_compress.main:main"
        ]
    }
)
