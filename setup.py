from setuptools import setup, find_packages

long_description_filename = "README.md"
try:
    with open(long_description_filename, "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = f"File {long_description_filename} not found"
except Exception:
    long_description = f"Failed to read {long_description_filename} because of unexpected error"

setup(
    # Project name (e. g. pip install proxmoxmanager)
    name="proxmoxmanager",

    # Current version
    version="1.0.4",

    # Short description
    description="Smart Proxmox VE API wrapper for managing resources automatically",

    # Long description
    long_description=long_description,

    # Long desctiption content type
    long_description_content_type="text/markdown",

    # Link to project's GitHub page
    url="https://github.com/igorlitvak/proxmoxmanager",

    # Project's author
    author="Igor Litvak, ITMO University",

    # Which packages are included
    packages=find_packages(),

    # Which Python version is required to run this project
    python_requires=">=3.7, <4",

    # Which external projects this project depends on
    install_requires=[
        "proxmoxer",
        "requests"
    ],

    # Metadata
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
)
