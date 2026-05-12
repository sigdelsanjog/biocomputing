"""
Example usage of biocomputing package
"""

from biocomputing.biocomputing import DNAGenerator, generate_sequential, generate_parallel


def main():
    """
    Demonstrate DNA generation with biocomputing package
    """
    
    print("=" * 70)
    print("biocomputing - DNA Generator Example")
    print("=" * 70)
    print()
    
    # Initialize generator
    try:
        gen = DNAGenerator()
        print("✓ DNA Generator initialized successfully\n")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        return
    
    # Test with different lengths
    test_cases = [
        (1000, "1K bases"),
        (100000, "100K bases"),
        (1000000, "1M bases"),
    ]
    
    print("Testing DNA Generation\n")
    
    for length, description in test_cases:
        print("-" * 70)
        print(f"Generating {description} ({length:,} bases)")
        print("-" * 70)
        
        # Sequential
        try:
            print("Sequential...", end=" ", flush=True)
            result = gen.generate_sequential(length)
            print(f"Done! ({result['time_taken']:.6f}s)")
            print(f"  First 50 bases: {result['sequence'][:50]}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Parallel
        try:
            print("Parallel...", end=" ", flush=True)
            result = gen.generate_parallel(length)
            print(f"Done! ({result['time_taken']:.6f}s)")
            print(f"  First 50 bases: {result['sequence'][:50]}")
        except Exception as e:
            print(f"Error: {e}")
        
        print()
    
    # Module-level functions
    print("=" * 70)
    print("Using convenience functions")
    print("=" * 70)
    print()
    
    length = 100000
    result_seq = generate_sequential(length)
    result_par = generate_parallel(length)
    
    print(f"Sequential: {result_seq['time_taken']:.6f}s")
    print(f"Parallel:   {result_par['time_taken']:.6f}s")
    print(f"Speedup:    {result_seq['time_taken']/result_par['time_taken']:.2f}x")
    
    print()
    print("✓ Example completed successfully!")


if __name__ == "__main__":
    main()
