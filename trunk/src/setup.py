'''
    Setup configuration for pypbald.
    
    Migrated from py2exe to setuptools for Python 3 compatibility.

    Author:
        Giovanni Novelli, Ph.D.
	giovanni.novelli@gmail.com
'''

__author__ = "Giovanni Novelli"
__date__ = "02/05/2010"

from setuptools import setup, find_packages

setup(
    name="pypbald",
    version="2.0.0",
    author="Giovanni Novelli",
    author_email="giovanni.novelli@gmail.com",
    description="Python network analysis tool for ARP and NBD packets",
    long_description="pypbald is a Python network analysis tool that captures and analyzes ARP (Address Resolution Protocol) and NBD (Network Block Device) packets.",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "dpkt>=1.9.0",
        "mysql-connector-python>=8.0.0",
    ],
    entry_points={
        'console_scripts': [
            'pypbald=main:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Networking :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)