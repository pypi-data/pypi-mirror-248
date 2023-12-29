# Python Sorting Library

[![PyPI](https://img.shields.io/pypi/v/pysortlib)](https://pypi.org/project/pysortlib)
[![Downloads](https://static.pepy.tech/badge/pysortlib)](https://pepy.tech/project/pysortlib)
[![Coverage](https://coveralls.io/repos/github/slimreaper35/pysortlib/badge.svg?branch=main)](https://coveralls.io/github/slimreaper35/pysortlib?branch=main)

**Sorting algorithms with precise implementation and documentation.**

Implemented:

- Bubble sort
- Counting sort
- Heap sort
- Insert sort
- Merge sort
- Pancake sort
- Quick sort
- Radix sort
- Selection sort
- Shell sort
- Sleep sort

Planned:

- Cycle sort

## Install

```bash
pip install pysortlib
```

## Usage

```python
from pysortlib import insert_sort

array = [3, 5, 2, 1, 7, 4, 6]
insert_sort(array)  # set a breakpoint and explore \o/
print(array)
```

## Development

### Virtual environment

```bash
pip install --user poetry
poetry config virtualenvs.in-project true
poety shell
poetry install
```

### Dependencies

```bash
poetry update
```

### Pre-commit

```bash
pre-commit clean
pre-commit install --hook-type pre-commit
```

### Coding standards

- ~~perfectionism~~
- [black](https://black.readthedocs.io/en/stable/) - code formatting
- [ruff](https://beta.ruff.rs/docs/) - static code analysis
- [mypy](https://mypy.readthedocs.io/en/stable/) - static type checking
- [pytest](https://docs.pytest.org/en/stable/) - unit tests

## License

This project is licensed under the terms of the MIT license.
