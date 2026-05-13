"""
Download pre-compiled C libraries from GitHub releases.
This script is run during pip install to fetch platform-specific .so files.
"""

import os
import platform
import shutil
import sys
import urllib.request
import urllib.error
import json
from pathlib import Path


def get_platform_name():
    """
    Detect the current platform and architecture.
    Returns a tuple of (os_name, arch).
    """
    system = platform.system()
    machine = platform.machine()
    
    # Map to standard naming
    if system == "Linux":
        if machine in ("x86_64", "AMD64"):
            return "linux", "x86_64"
        elif machine in ("aarch64", "arm64"):
            return "linux", "aarch64"
        elif machine == "armv7l":
            return "linux", "armv7l"
    elif system == "Darwin":  # macOS
        if machine == "x86_64":
            return "macos", "x86_64"
        elif machine == "arm64":
            return "macos", "aarch64"
    elif system == "Windows":
        if machine in ("x86_64", "AMD64"):
            return "windows", "x86_64"
    
    return None, None


def get_latest_release_tag(github_repo):
    """
    Fetch the latest release tag from GitHub API.
    
    Args:
        github_repo: Repository in format "owner/repo"
        
    Returns:
        str: Latest tag name (e.g., "v1.0.5"), or None if failed
    """
    api_url = f"https://api.github.com/repos/{github_repo}/releases/latest"
    try:
        print(f"Fetching latest release from {github_repo}...")
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode('utf-8'))
            tag_name = data.get('tag_name')
            if tag_name:
                print(f"✓ Latest release: {tag_name}")
                return tag_name
            else:
                print("✗ No tag_name found in release")
                return None
    except Exception as e:
        print(f"✗ Failed to fetch latest release: {e}")
        return None


def download_file(url, destination, timeout=30):
    """Download a file from URL with error handling."""
    try:
        print(f"Downloading: {url}")
        # Use urlopen with timeout instead of urlretrieve
        with urllib.request.urlopen(url, timeout=timeout) as response:
            with open(destination, 'wb') as out_file:
                out_file.write(response.read())
        print(f"✓ Downloaded to: {destination}")
        return True
    except urllib.error.URLError as e:
        print(f"✗ Download failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during download: {e}")
        return False


def download_libraries(github_repo="sigdelsanjog/biocomputing_core", 
                      release_tag="latest",
                      target_dir=None):
    """
    Download pre-compiled libraries from GitHub releases.
    
    Args:
        github_repo: Repository in format "owner/repo"
        release_tag: GitHub release tag (default: "latest")
        target_dir: Directory to save libraries (default: biocomputing/_lib)
    """
    
    # If "latest" is requested, fetch the actual latest tag from GitHub API
    if release_tag == "latest":
        actual_tag = get_latest_release_tag(github_repo)
        if actual_tag:
            release_tag = actual_tag
        else:
            print("⚠ Could not determine latest release tag. Using 'latest' (may fail)")
    
    os_name, arch = get_platform_name()
    
    if not os_name or not arch:
        print(f"⚠ Unsupported platform: {platform.system()} {platform.machine()}")
        return False
    
    print(f"Platform detected: {os_name}-{arch}")
    
    if target_dir is None:
        target_dir = Path(__file__).parent / "_lib"
    else:
        target_dir = Path(target_dir)
    
    # Create target directory
    target_dir.mkdir(exist_ok=True, parents=True)
    
    # Library names to download
    libraries = [
        "libdna_sequential.so",
        "libdna_parallel.so"
    ]
    
    base_url = f"https://github.com/{github_repo}/releases/download/{release_tag}"
    all_success = True
    
    for lib_name in libraries:
        # Construct platform-specific name
        lib_base = lib_name.replace(".so", "")
        platform_lib_name = f"{lib_base}_{os_name}_{arch}.so"
        
        url = f"{base_url}/{platform_lib_name}"
        destination = target_dir / lib_name
        
        # Check if already exists and is valid
        if destination.exists():
            print(f"✓ Library already exists: {lib_name}")
            continue
        
        # Download the library
        if not download_file(url, str(destination)):
            print(f"✗ Failed to download {lib_name}")
            all_success = False
            # Cleanup partial downloads
            if destination.exists():
                destination.unlink()
    
    return all_success


def verify_libraries(target_dir=None):
    """Verify that all required libraries are present."""
    if target_dir is None:
        target_dir = Path(__file__).parent / "_lib"
    else:
        target_dir = Path(target_dir)
    
    required_libs = ["libdna_sequential.so", "libdna_parallel.so"]
    
    for lib in required_libs:
        lib_path = target_dir / lib
        if not lib_path.exists():
            return False, lib
    
    return True, None


if __name__ == "__main__":
    success = download_libraries()
    sys.exit(0 if success else 1)
