import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "nmse_utils-kwhitham",
    version = "0.0.1",
    author = "Kevin Whitham",
    author_email = "kwhitham@lbl.gov",
    description = "Routines to access NMSE 2D perovskite data files",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/kwhitham/nmse_utils",
    classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approvied :: GNU General PUblic License v3 or later (GPLv3+)",
            "Operating System :: OS Independent",
    ],

    package_dir = {"","src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.8.5",
)
