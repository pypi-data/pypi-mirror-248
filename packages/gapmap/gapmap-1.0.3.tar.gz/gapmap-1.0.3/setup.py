from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = "1.0.3"
AUTHOR = "Paul Gardiner"
AUTHOR_EMAIL = "franticstone@gmail.com"
APP_NAME = "gapmap"
DESCRIPTION = "Maptools"

setup(
    name=APP_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email=AUTHOR_EMAIL,
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    keywords=["radius", "point", "mathlib"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
