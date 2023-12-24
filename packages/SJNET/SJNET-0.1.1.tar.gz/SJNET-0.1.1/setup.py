import pathlib

import setuptools
import pathlib
import setuptools

setuptools.setup(
    name="SJNET",
    version="0.1.1",
    description="A neural network Framework",
    author="Abhijith SJ",
    author_email="sjabhijith187@gmail.com",
    classifiers=["Topic :: Scientific/Engineering :: Artificial Intelligence","Development Status :: 5 - Production/Stable","Programming Language :: Python :: 3.10","Programming Language :: Python :: 3.11"],
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown"
    )
