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
    """Custom install command that downloads C libraries from GitHub."""
    
    def run(self):
        """Run the standard install, then download libraries."""
        print("\n" + "="*70)
        print("Biocomputing: Downloading pre-compiled C libraries from GitHub...")
        print("="*70 + "\n")
        
        try:
            from biocomputing.biocomputing.download_libs import download_libraries, verify_libraries
            
            # Get the biocomputing package directory
            biocomputing_dir = Path(__file__).parent / "biocomputing"
            lib_dir = biocomputing_dir / "_lib"
            
            # Download libraries
            success = download_libraries(
                github_repo="sigdelsanjog/biocomputing_core",
                release_tag="latest",
                target_dir=str(lib_dir)
            )
            
            if not success:
                print("\n⚠ Warning: Some libraries failed to download")
                print("   The package may not work correctly without these libraries")
                print("   You can manually download from:")
                print("   https://github.com/sigdelsanjog/biocomputing_core/releases\n")
            
            # Verify libraries are present
            verified, missing_lib = verify_libraries(target_dir=str(lib_dir))
            if not verified:
                print(f"\n⚠ Warning: Missing library {missing_lib}")
                print("   Please ensure all libraries are present in biocomputing/_lib/\n")
            else:
                print("\n✓ All libraries verified successfully!\n")
        
        except ImportError as e:
            print(f"⚠ Could not import download module: {e}")
            print("  Attempting to continue with installation anyway...\n")
        except Exception as e:
            print(f"⚠ Error during library download: {e}")
            print("  Continuing with installation...\n")
        
        # Run the standard install
        super().run()


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
    package_data={
        "biocomputing": ["_lib/*.so"],  # Include .so files in package
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
