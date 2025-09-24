#!/usr/bin/env python3
"""Setup script for MODBUSTCP application."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="modbustcp-service",
    version="1.0.0",
    author="DevonixCompany",
    author_email="dev@devonixcompany.com",
    description="Production-ready MODBUS TCP service with clean architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devonixcompany/MODBUSTCP",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Hardware",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "modbustcp=presentation.cli.main:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)