# Perfwatch

Perfwatch is a python package that allows you to monitor the performance of your code. It is designed to be used in a Jupyter notebook, but can also be used in a Python script.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [Usage](#usage)
    - [Available Profiler Types](#available-profiler-types)
    - [Basic Usage](#basic-usage)
    - [Customizing Profiling](#customizing-profiling)
    - [Logging](#logging)
- [License](#license)

## Installation

To install perfwatch, run the following command:

```bash
pip install perfwatch
```

## Development

To install perfwatch for development, clone the repository and run the following command:

```bash
poetry install
```
To setup pre-commit hooks, run the following command:

```bash
poetry run pre-commit install
```

To run the tests, run the following command:

```bash
poetry run pytest
```

## Usage

### Available Profiler Types

The profiler supports the following profiler types:

-   `cpu`: Profiles CPU usage using the `cProfile` module.
-   `memory`: Profiles memory usage using the `memory_profiler` module.
-   `thread`: Profiles thread creation and usage.
-   `io`: Profiles I/O operations.
-   `network`: Profiles network traffic using the `NetworkProfiler` class.
-   `gpu`: Profiles GPU usage using the `GPUProfiler` class.
-   `cache`: Profiles cache performance (not implemented).
-   `exception`: Profiles exception handling (not implemented).
-   `system`: Profiles system performance (not implemented).
-   `distributed`: Profiles distributed system performance (not implemented).
-   `line`: Profiles line-by-line execution using the `line_profiler` module.
-   `time`: Profiles execution time.


### Basic Usage
```python
from perfwatch import watch

@watch(["line", "cpu", "time"])
def test():
    for _ in range(1000000):
        pass

if __name__ == "__main__":
    test()
```

#### Customizing Profiling

You can customize the profiling behavior by passing additional keyword arguments to the `watch` decorator. For example:

```python
@watch("network", packet_src="localhost")
def my_function(x, y):
    # function implementation
    pass
```

#### Logging

The Profiler Service uses a logger to output profiling results. You can specify a log file path using the log_file_path keyword argument:

```python
@watch("cpu", log_file_path="profiling.log")
def my_function(x, y):
    # function implementation
    pass
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
