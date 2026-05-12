# biocomputing

High-performance DNA sequence generator Python package with sequential and parallel (OpenMP) implementations.

[![GitHub](https://img.shields.io/badge/github-sigdelsanjog/biocomputing-blue?logo=github)](https://github.com/sigdelsanjog/biocomputing)
[![C Backend](https://img.shields.io/badge/C%20Backend-biocomputing_core-orange)](https://github.com/sigdelsanjog/biocomputing_core)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Features

- ⚡ **High Performance**: Compiled C backend for fast DNA generation
- 🔄 **Parallel Processing**: OpenMP support for multi-threaded execution
- 🐍 **Easy to Use**: Simple Python API
- 📦 **Pip Installable**: Standard Python package installation
- 🔗 **Modular**: Separate C and Python packages for flexibility

## Installation

### Prerequisites

You need build tools and OpenMP:

```bash
# Ubuntu/Debian
sudo apt-get install build-essential libomp-dev

# macOS
brew install gcc libomp

# Fedora/RHEL
sudo dnf install gcc gcc-c++ libomp-devel
```

### Install via Pip

```bash
pip install biocomputing
```

### Install from Source

1. Clone the C backend:

```bash
git clone https://github.com/sigdelsanjog/biocomputing_core.git
cd biocomputing_core
make
cd ..
```

2. Clone and install the Python package:

```bash
git clone https://github.com/sigdelsanjog/biocomputing.git
cd biocomputing
pip install -e .
```

## Quick Start

### Basic Usage

```python
from biocomputing import DNAGenerator

# Initialize generator
gen = DNAGenerator()

# Generate 1 million bases sequentially
result = gen.generate_sequential(1000000)
print(f"Generated {len(result['sequence'])} bases in {result['time_taken']:.4f}s")
print(f"First 100 bases: {result['sequence'][:100]}")

# Generate 1 million bases in parallel
result = gen.generate_parallel(1000000)
print(f"Generated {len(result['sequence'])} bases in {result['time_taken']:.4f}s")
```

### Using Convenience Functions

```python
from biocomputing import generate_sequential, generate_parallel

# Simple function-based API
result_seq = generate_sequential(500000)
result_par = generate_parallel(500000)
```

### Return Value Format

Both functions return a dictionary:

```python
{
    'sequence': str,          # Generated DNA sequence (A, T, G, C)
    'time_taken': float,      # Execution time in seconds
    'method': str            # Either 'sequential' or 'parallel'
}
```

## Performance

The parallel implementation typically provides significant speedup for large sequences. Performance depends on:

- Sequence length (larger is better for parallelism)
- Number of CPU cores available
- System load

### Example Performance (12-core system)

| Length | Sequential | Parallel | Speedup |
| ------ | ---------- | -------- | ------- |
| 1M     | 0.015s     | 0.002s   | 7.5x    |
| 10M    | 0.15s      | 0.02s    | 7.5x    |
| 100M   | 1.5s       | 0.2s     | 7.5x    |

## API Reference

### Class: `DNAGenerator`

#### Methods

**`generate_sequential(length: int) -> dict`**

- Generate DNA sequence using single thread
- **Args**: `length` - number of bases to generate
- **Returns**: dict with 'sequence', 'time_taken', 'method'
- **Raises**: MemoryError if allocation fails

**`generate_parallel(length: int) -> dict`**

- Generate DNA sequence using all available CPU cores
- **Args**: `length` - number of bases to generate
- **Returns**: dict with 'sequence', 'time_taken', 'method'
- **Raises**: MemoryError if allocation fails

### Module Functions

**`generate_sequential(length: int) -> dict`**

- Convenience function (auto-initializes generator)

**`generate_parallel(length: int) -> dict`**

- Convenience function (auto-initializes generator)

## Architecture

```
biocomputing (Python Package)
├── __init__.py
├── wrapper.py (ctypes wrapper)
├── setup.py
└── Tests & Examples

       ↓ calls ↓

biocomputing_core (C Library)
├── dna_generator.h (API)
├── sequential_sequence_generator.c
├── parallel_sequence_generator.c
└── Makefile
```

## Troubleshooting

### Error: "Library not found"

**Solution**: Build the C backend:

```bash
cd ../biocomputing_core
make
```

### Error: "Module not found"

**Solution**: Install the package:

```bash
pip install -e .
```

### Parallel slower than sequential

**Causes**:

- Sequence too small (overhead > gains)
- Try with sequences >100K bases
- Check CPU usage with `htop`

### Memory errors with huge sequences

**Solution**: Use multiple smaller generations:

```python
sequences = []
for _ in range(10):
    result = gen.generate_parallel(100000000)  # 100M at a time
    sequences.append(result['sequence'])
full_sequence = ''.join(sequences)
```

## Development

### Setup Development Environment

```bash
git clone https://github.com/sigdelsanjog/biocomputing.git
cd biocomputing
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Style

```bash
black biocomputing/
flake8 biocomputing/
```

## Architecture Details

### ctypes Bridge

The Python wrapper uses Python's standard `ctypes` library to call C functions:

1. **Dynamic Loading**: `.so` files are loaded at runtime
2. **Type Mapping**: Python types are converted to C types
3. **Memory Management**: Automatic cleanup via wrapper functions

### Thread Safety

- Sequential version: No concurrency issues
- Parallel version: Thread-safe via OpenMP's internal management

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) file

## References

- [biocomputing_core](https://github.com/sigdelsanjog/biocomputing_core) - C backend
- [ctypes Documentation](https://docs.python.org/3/library/ctypes.html)
- [OpenMP Documentation](https://www.openmp.org/)

## Author

**Sanjog Sigdel**

- GitHub: [@sigdelsanjog](https://github.com/sigdelsanjog)
- Email: sigdelsanjog@example.com

## Related Projects

- **biocomputing_core**: C library backend
- **bioinfo**: Original bioinfo project

---

Made with ❤️ for bioinformatics research
