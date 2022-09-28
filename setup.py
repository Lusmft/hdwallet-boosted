#!/usr/bin/env python3

from setuptools import (
    setup, find_packages
)

# Project URLs
project_urls = {
    "Tracker": "https://github.com/baffolobill/python-hdwallet-boosted/issues",
}

# README.md
with open("README.md", "r", encoding="utf-8") as readme:
    long_description: str = readme.read()


setup(
    name="hdwallet_boosted",
    version="1.0.0",
    description="Speeds up python-hdwallet by replacing the elliptic curve math "
                "from pure python to the heavily optimized C library libsecp256k1.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Alexander Volkov",
    author_email="baffolobill@yandex.ru",
    url="https://github.com/baffolobill/python-hdwallet-boosted",
    project_urls=project_urls,
    keywords=[
        "cryptography", "wallet", "bip32", "bip44", "bip39", "hdwallet", 
        "cryptocurrency", "bitcoin", "ethereum", "secp256k1",
    ],
    python_requires=">=3.6,<4",
    packages=find_packages(),
    install_requires=[
        'hdwallet>=2.1.1,<2.2', 
        'coincurve>=17.0.0,<17.1',
    ],
    extras_require={
        "tests": [
            "pytest>=6.2.5,<7",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
