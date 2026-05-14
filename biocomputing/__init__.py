"""
biocomputing - High-performance DNA sequence generation

Python package providing easy access to fast DNA sequence generation
with both sequential and parallel (OpenMP) implementations.

Usage:
    from biocomputing import DNAGenerator
    
    gen = DNAGenerator()
    result = gen.generate_parallel(1000000)
    print(result['sequence'][:100])
"""

__version__ = "1.0.0"
__author__ = "Sanjog Sigdel"
__email__ = "sigdelsanjog@example.com"

from .wrapper import (
    DNAGenerator, 
    generate_sequential, 
    generate_parallel,
    calculate_gc_content,
    calculate_gc_content_batch
)

__all__ = [
    "DNAGenerator", 
    "generate_sequential", 
    "generate_parallel",
    "calculate_gc_content",
    "calculate_gc_content_batch"
]
