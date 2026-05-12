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
