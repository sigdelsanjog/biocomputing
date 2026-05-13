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
        """Run the standard install and verify libraries."""
        print("\n" + "="*70)
        print("Biocomputing: Checking C libraries...")
        print("="*70 + "\n")
        
        # Get the _lib directory
        lib_dir = Path(__file__).parent / "biocomputing" / "_lib"
        
        # Required libraries
        required_libs = [
            "libdna_sequential.so",
            "libdna_parallel.so"
        ]
        
        # Create _lib directory if it doesn't exist
        lib_dir.mkdir(exist_ok=True, parents=True)
        
        print(f"Library directory: {lib_dir}\n")
        print("Shared Object Status:")
        print("-" * 70)
        
        all_present = True
        for lib_name in required_libs:
            lib_path = lib_dir / lib_name
            if lib_path.exists():
                file_size = lib_path.stat().st_size
                size_mb = file_size / (1024 * 1024)
                print(f"✓ {lib_name:<30} {size_mb:>8.2f} MB  [{lib_path}]")
            else:
                print(f"✗ {lib_name:<30} {'NOT FOUND':<10}  [{lib_path}]")
                all_present = False
        
        print("-" * 70)
        
        if all_present:
            print("\n✓ All required shared objects are present!\n")
        else:
            print("\n⚠ Warning: Some shared objects are missing!")
            print("   The biocomputing package will try to download them.")
            print("   Make sure you have internet access.\n")
            
            # Try to download missing libraries
            try:
                from biocomputing.download_libs import download_libraries, verify_libraries
                
                print("Attempting to download libraries from GitHub...")
                success = download_libraries(
                    github_repo="sigdelsanjog/biocomputing_core",
                    release_tag="latest",
                    target_dir=str(lib_dir)
                )
                
                if success:
                    print("\n✓ Libraries downloaded successfully!\n")
                else:
                    print("\n⚠ Failed to download some libraries.")
                    print("   You can manually download from:")
                    print("   https://github.com/sigdelsanjog/biocomputing_core/releases\n")
            except Exception as e:
                print(f"\n⚠ Could not download libraries: {e}")
                print("   Manual download may be required.\n")
        
        print("=" * 70)
        print("Proceeding with installation...\n")
        
        # Run the standard install
        super().run()


setup(
    name="biocomputing",
    version="1.0.4",
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
