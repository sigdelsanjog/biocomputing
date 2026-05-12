# GitHub Deployment Guide

This guide explains how to set up both `biocomputing_core` (C package) and `biocomputing` (Python package) on GitHub.

## Repository Structure

```
Your Local Development:
├── biocomputing_core/     (C package)
│   ├── *.c files
│   ├── *.h files
│   ├── Makefile
│   ├── README.md
│   ├── LICENSE
│   └── .gitignore
│
└── biocomputing/          (Python package)
    ├── biocomputing/
    │   ├── __init__.py
    │   └── wrapper.py
    ├── setup.py
    ├── pyproject.toml
    ├── README.md
    ├── LICENSE
    ├── .gitignore
    └── example.py

GitHub Repositories:
├── github.com/sigdelsanjog/biocomputing_core
└── github.com/sigdelsanjog/biocomputing
```

## Step 1: Create GitHub Repositories

### biocomputing_core (C Package)

1. Go to https://github.com/new
2. Create repository: `biocomputing_core`
3. Description: "High-performance DNA sequence generator C library"
4. Public
5. **Do NOT initialize** (we'll push from local)

### biocomputing (Python Package)

1. Go to https://github.com/new
2. Create repository: `biocomputing`
3. Description: "Python package for fast DNA sequence generation"
4. Public
5. **Do NOT initialize** (we'll push from local)

## Step 2: Initialize Git Repositories Locally

### For biocomputing_core (C Package)

```bash
cd ~/Documents/proj/py\ Snippet/BICP\ 406/biocomputing_core

# Initialize git
git init

# Configure user
git config user.name "Sanjog Sigdel"
git config user.email "sigdelsanjog@example.com"

# Add all files
git add .

# First commit
git commit -m "Initial commit: DNA Generator C library with OpenMP support"

# Add remote
git remote add origin https://github.com/sigdelsanjog/biocomputing_core.git

# Rename branch if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

### For biocomputing (Python Package)

```bash
cd ~/Documents/proj/py\ Snippet/BICP\ 406/biocomputing

# Initialize git
git init

# Configure user
git config user.name "Sanjog Sigdel"
git config user.email "sigdelsanjog@example.com"

# Add all files
git add .

# First commit
git commit -m "Initial commit: Python wrapper for DNA Generator library"

# Add remote
git remote add origin https://github.com/sigdelsanjog/biocomputing.git

# Rename branch if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 3: Verify Repositories

Visit:

- https://github.com/sigdelsanjog/biocomputing_core
- https://github.com/sigdelsanjog/biocomputing

## Step 4: Build and Test Locally

### Build C Libraries

```bash
cd ~/Documents/proj/py\ Snippet/BICP\ 406/biocomputing_core
make
```

### Install Python Package Locally

```bash
cd ~/Documents/proj/py\ Snippet/BICP\ 406/biocomputing
pip install -e .
```

### Test

```bash
python example.py
```

## Step 5: Publish to PyPI (Optional)

To make `pip install biocomputing` work globally:

```bash
# Install build tools
pip install build twine

# Build package
cd ~/Documents/proj/py\ Snippet/BICP\ 406/biocomputing
python -m build

# Create PyPI account at https://pypi.org/account/register/

# Upload (requires PyPI API token)
twine upload dist/*
```

## Step 6: GitHub Release & Tags

### Create Release for biocomputing_core

```bash
cd ~/Documents/proj/py\ Snippet/BICP\ 406/biocomputing_core

# Create tag
git tag -a v1.0.0 -m "First stable release"

# Push tag
git push origin v1.0.0
```

### Create Release for biocomputing

```bash
cd ~/Documents/proj/py\ Snippet/BICP\ 406/biocomputing

# Create tag
git tag -a v1.0.0 -m "First stable release"

# Push tag
git push origin v1.0.0
```

Then create releases on GitHub (Releases tab) for both.

## Documentation URLs

After setup, these will be available:

- **C Package Repo**: https://github.com/sigdelsanjog/biocomputing_core
- **Python Package Repo**: https://github.com/sigdelsanjog/biocomputing
- **Python Package on PyPI**: https://pypi.org/project/biocomputing/

## Making Changes

### To biocomputing_core (C code):

```bash
cd ~/Documents/proj/py\ Snippet/BICP\ 406/biocomputing_core
# Make changes
git add .
git commit -m "Your message"
git push
```

### To biocomputing (Python code):

```bash
cd ~/Documents/proj/py\ Snippet/BICP\ 406/biocomputing
# Make changes
git add .
git commit -m "Your message"
git push
```

## CI/CD Automation (Optional)

Create [`.github/workflows/publish.yml`](../.github/workflows/publish.yml) for automatic PyPI publishing on tag creation.

## Troubleshooting

### "fatal: not a git repository"

```bash
git init
git remote add origin https://github.com/sigdelsanjog/biocomputing.git
```

### "fatal: 'origin' does not appear to be a 'git' repository"

```bash
git remote set-url origin https://github.com/sigdelsanjog/biocomputing.git
```

### Permission denied (publickey)

Set up SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

---

Now your two packages are properly organized for professional development and distribution! 🚀
