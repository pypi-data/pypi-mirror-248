#!/usr/bin/env python
import sys

from setuptools import setup
from setuptools_rust import RustExtension

setup(
    name="hmt-lzma-pyo3",
    version="0.1.0",
    description="Python module based on the LZ-String javascript, purpose here is to be faster than existing native python implementation",
    long_description="Python module based on the LZ-String javascript, purpose here is to be faster than existing native python implementation",
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Rust",
        "Operating System :: POSIX"
    ],
    packages=["lzma_pyo3"],
    rust_extensions=[RustExtension("lzma_pyo3.lzma_pyo3")],
    include_package_data=True,
    zip_safe=False,
)