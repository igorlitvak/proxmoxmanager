from setuptools import setup, find_packages

with open("requirements.txt") as f:
    REQUIREMENTS = f.read().splitlines()

setup(
    # Project name (e. g. pip install proxmoxmanager)
    name="proxmoxmanager",

    # Current version
    version="0.0.1",

    # Short description
    description="Smart Proxmox VE API wrapper for automatically managing resources",

    # Long description
    long_description="",  # TODO: add full description

    # Link to project's GitHub page
    url="https://github.com/igorlitvak/proxmoxmanager",

    # Project's author
    author="Igor Litvak, ITMO University",

    # Which packages are included
    packages=find_packages(where="proxmoxmanager"),

    # Which Python version is required to run this project
    python_requires=">=3.8, <4",  # TODO: test on earlier versions

    # Which external projects this project depends on
    install_requires=REQUIREMENTS,
)
