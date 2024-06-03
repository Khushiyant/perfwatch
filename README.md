# Perfwatch

Perfwatch is a python package that allows you to monitor the performance of your code. It is designed to be used in a Jupyter notebook, but can also be used in a Python script.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

To install perfwatch, run the following command:

```bash
pip install perfwatch
```

## Usage

```python
from perfwatch import PerformanceProfiler

@PerformanceProfiler.performance_profile
def test():
    for _ in range(1000000):
        pass

if __name__ == "__main__":
    test()
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
