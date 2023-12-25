import setuptools
from pathlib import Path

setuptools.setup(
    name="bradensolarcalc",
    version=1.0,
    long_description="",
    packages=setuptools.find_packages(exclude=(["data", "tests"]))
)
