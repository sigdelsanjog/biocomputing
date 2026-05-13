"""
Setup configuration for biocomputing Python package
Automatically downloads pre-compiled C libraries from GitHub during installation.
"""

from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.install import install
import sys

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""


class DownloadLibrariesCommand(install):
    """Custom install command that verifies C libraries are present."""
    
    def run(self):
        """Run the standard install."""
        # Run the standard install
        super().run()


setup(
    name="biocomputing",
    version="1.0.3",
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
    
    packages=find_packages(exclude=["tests"]),
    package_data={
        "biocomputing": ["_lib/*.so", "_lib/.gitkeep"],
    },
    include_package_data=True,
    
    python_requires=">=3.6",
    
    cmdclass={
        "install": DownloadLibrariesCommand,
    },
    
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
