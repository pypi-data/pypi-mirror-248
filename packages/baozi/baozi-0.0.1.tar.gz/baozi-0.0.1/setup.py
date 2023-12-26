import pathlib

from setuptools import find_packages, setup

PROJECT_NAME = "baozi"
PROJECT_ROOT = pathlib.Path.cwd()
VERSION = "0.0.1"

import codecs

with codecs.open(str(PROJECT_ROOT / "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name=PROJECT_NAME,
    version=VERSION,
    package_dir={"": "baozi"},
    packages=find_packages(where="baozi"),
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="race",
    author_email="raceychan@gmail.com",
    license="MIT",
    python_requires=">=3.11",
)
