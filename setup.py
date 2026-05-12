"""
Setup configuration for biocomputing Python package
"""

from pathlib import Path
from setuptools import setup, find_packages

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="biocomputing",
    version="1.0.0",
    author="Sanjog Sigdel",
    author_email="sigdelsanjog@example.com",
    description="High-performance DNA sequence generator with Python bindings (Sequential & Parallel)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sigdelsanjog/biocomputing",
    project_urls={
        "Bug Tracker": "https://github.com/sigdelsanjog/biocomputing/issues",
        "Source Code": "https://github.com/sigdelsanjog/biocomputing",
        "C Backend": "https://github.com/sigdelsanjog/biocomputing_core",
    },
    
    packages=find_packages(),
    py_modules=["biocomputing"],
    
    python_requires=">=3.6",
    
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    
    keywords="dna generator bioinformatics parallel sequential openmp",
)
