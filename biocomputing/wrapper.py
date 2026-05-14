"""
DNA Generator Python Wrapper
This module provides Python bindings to C DNA generator libraries using ctypes.
"""

import ctypes
import os
import sys
from pathlib import Path

# Get the directory where the shared libraries are located
# First, try to find pre-downloaded libraries in the package _lib directory
_PACKAGE_DIR = Path(__file__).parent
_LIB_DIR = _PACKAGE_DIR / "_lib"

# Fallback to biocomputing_core directory if _lib doesn't exist
# (for local development without pip install)
if not _LIB_DIR.exists():
    _LIB_DIR = Path(__file__).parent.parent / "biocomputing_core"


def _ensure_libraries_available():
    """
    Ensure that the required .so files are available.
    Download them if they don't exist.
    """
    required_libs = ["libdna_sequential.so", "libdna_parallel.so"]
    
    # Check if all libraries exist
    all_present = True
    for lib_name in required_libs:
        if not (_LIB_DIR / lib_name).exists():
            all_present = False
            break
    
    # If all present, we're good
    if all_present:
        return True
    
    # Try to download missing libraries
    try:
        from . import download_libs
        
        print("\n" + "="*70)
        print("Biocomputing: Downloading C libraries from GitHub...")
        print("="*70)
        
        success = download_libs.download_libraries(
            github_repo="sigdelsanjog/biocomputing_core",
            release_tag="latest",
            target_dir=str(_LIB_DIR)
        )
        
        if success:
            print("="*70 + "\n")
            return True
        else:
            print("="*70 + "\n")
            return False
            
    except Exception as e:
        print(f"\nWarning: Could not download libraries: {e}\n")
        return False


# Ensure libraries are available when wrapper is imported
_ensure_libraries_available()

# Define the return structure
class DNAResult(ctypes.Structure):
    _fields_ = [
        ("sequence", ctypes.POINTER(ctypes.c_char)),
        ("time_taken", ctypes.c_double),
    ]


class DNAGenerator:
    """
    DNA Generator class that provides access to sequential and parallel
    DNA sequence generation functions from C libraries.
    """
    
    def __init__(self):
        """Initialize and load the C libraries."""
        self.seq_lib = self._load_library("libdna_sequential.so")
        self.par_lib = self._load_library("libdna_parallel.so")
        
        if self.seq_lib:
            self._setup_sequential()
        if self.par_lib:
            self._setup_parallel()
    
    def _load_library(self, lib_name):
        """Load a shared library from the _lib directory."""
        lib_path = _LIB_DIR / lib_name
        
        if not lib_path.exists():
            error_msg = (
                f"Library {lib_name} not found at {lib_path}\n\n"
                f"To fix this issue, you have two options:\n"
                f"1. Install via pip (recommended):\n"
                f"   pip install biocomputing\n\n"
                f"2. For local development:\n"
                f"   - Clone the biocomputing_core repository\n"
                f"   - Run: make -C biocomputing_core\n"
                f"   - Libraries will be auto-detected\n\n"
                f"Repository: https://github.com/sigdelsanjog/biocomputing_core"
            )
            raise FileNotFoundError(error_msg)
        
        try:
            return ctypes.CDLL(str(lib_path))
        except OSError as e:
            raise RuntimeError(f"Failed to load library {lib_name}: {e}")
    
    def _setup_sequential(self):
        """Configure the sequential generator function signature."""
        self.seq_lib.generate_dna_sequential.argtypes = [ctypes.c_ulong]
        self.seq_lib.generate_dna_sequential.restype = DNAResult
        self.seq_lib.free_dna_result.argtypes = [ctypes.POINTER(DNAResult)]
    
    def _setup_parallel(self):
        """Configure the parallel generator function signature."""
        self.par_lib.generate_dna_parallel.argtypes = [ctypes.c_ulong]
        self.par_lib.generate_dna_parallel.restype = DNAResult
        self.par_lib.free_dna_result.argtypes = [ctypes.POINTER(DNAResult)]
    
    def generate_sequential(self, length):
        """
        Generate DNA sequence sequentially.
        
        Args:
            length (int): Length of the DNA sequence to generate
            
        Returns:
            dict: Dictionary with keys 'sequence' and 'time_taken'
        """
        if not self.seq_lib:
            raise RuntimeError("Sequential library not loaded")
        
        result = self.seq_lib.generate_dna_sequential(ctypes.c_ulong(length))
        
        if result.time_taken < 0:
            raise MemoryError("Failed to allocate memory for DNA sequence")
        
        # Convert C string to Python string
        sequence = ctypes.string_at(result.sequence, length).decode('ascii')
        time_taken = result.time_taken
        
        # Free the C memory
        self.seq_lib.free_dna_result(ctypes.byref(result))
        
        return {
            'sequence': sequence,
            'time_taken': time_taken,
            'method': 'sequential'
        }
    
    def generate_parallel(self, length):
        """
        Generate DNA sequence using parallel processing (OpenMP).
        
        Args:
            length (int): Length of the DNA sequence to generate
            
        Returns:
            dict: Dictionary with keys 'sequence' and 'time_taken'
        """
        if not self.par_lib:
            raise RuntimeError("Parallel library not loaded")
        
        result = self.par_lib.generate_dna_parallel(ctypes.c_ulong(length))
        
        if result.time_taken < 0:
            raise MemoryError("Failed to allocate memory for DNA sequence")
        
        # Convert C string to Python string
        sequence = ctypes.string_at(result.sequence, length).decode('ascii')
        time_taken = result.time_taken
        
        # Free the C memory
        self.par_lib.free_dna_result(ctypes.byref(result))
        
        return {
            'sequence': sequence,
            'time_taken': time_taken,
            'method': 'parallel'
        }


# Module-level convenience functions
_generator = None

def _get_generator():
    """Lazy load the generator instance."""
    global _generator
    if _generator is None:
        _generator = DNAGenerator()
    return _generator

def generate_sequential(length):
    """Generate DNA sequence sequentially."""
    return _get_generator().generate_sequential(length)

def generate_parallel(length):
    """Generate DNA sequence using parallel processing."""
    return _get_generator().generate_parallel(length)


# ============================================================================
# GC Content Calculator Functions
# ============================================================================

def calculate_gc_content(sequence: str) -> float:
    """
    Calculate the GC content of a DNA sequence.
    
    GC content is the percentage of G (guanine) and C (cytosine) nucleotides 
    in a DNA sequence. This is a key metric in genomic analysis.
    
    Args:
        sequence (str): DNA sequence containing A, T, G, C nucleotides
        
    Returns:
        float: GC content as a percentage (0-100)
        
    Raises:
        ValueError: If sequence is empty or contains invalid nucleotides
        
    Examples:
        >>> calculate_gc_content("ATGC")
        50.0
        >>> calculate_gc_content("GGGGCCCC")
        100.0
        >>> calculate_gc_content("AAAA")
        0.0
    """
    if not sequence:
        raise ValueError("Sequence cannot be empty")
    
    # Convert to uppercase for case-insensitive matching
    seq_upper = sequence.upper()
    
    # Validate sequence contains only valid nucleotides
    valid_nucleotides = set("ATGCN")
    if not all(n in valid_nucleotides for n in seq_upper):
        invalid_chars = set(seq_upper) - valid_nucleotides
        raise ValueError(f"Invalid nucleotides in sequence: {invalid_chars}")
    
    # Count G and C (excluding N which is unknown)
    gc_count = seq_upper.count('G') + seq_upper.count('C')
    total_count = len(seq_upper)
    
    # Calculate percentage
    gc_percent = (gc_count / total_count) * 100
    
    return gc_percent


def calculate_gc_content_batch(sequences: list) -> list:
    """
    Calculate GC content for multiple sequences.
    
    Efficiently processes a list of DNA sequences and returns GC content
    for each one. Errors for individual sequences don't stop processing.
    
    Args:
        sequences (list): List of DNA sequence strings
        
    Returns:
        list: List of dictionaries with keys 'sequence', 'gc_content', 
              'length' (or 'error' if there was a validation error)
        
    Examples:
        >>> seqs = ["ATGC", "GGGG"]
        >>> results = calculate_gc_content_batch(seqs)
        >>> len(results)
        2
        >>> results[0]['gc_content']
        50.0
    """
    results = []
    for sequence in sequences:
        try:
            gc = calculate_gc_content(sequence)
            results.append({
                "sequence": sequence,
                "gc_content": gc,
                "length": len(sequence)
            })
        except ValueError as e:
            results.append({
                "sequence": sequence,
                "error": str(e)
            })
    
    return results
