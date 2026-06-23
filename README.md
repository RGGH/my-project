# Python Project Structure: Simple vs "Proper" Package Layout

## What We Built

We created a small Python project using `uv` and `pytest`.

Initial structure:

```text
.
├── main.py
├── pyproject.toml
├── src
│   ├── __init__.py
│   └── utils.py
└── tests
    └── test_utils.py
```

The `utils.py` module contains reusable functions:

* `clamp()`
* `word_count()`
* `running_average()`

We then imported and used those functions from `main.py`, and configured `pytest` through `pyproject.toml`.

---

# Two Ways to Configure `pyproject.toml`

There are two common approaches.

---

# Option 1: Simple Project (no package build)

Good for learning, scripts, and small projects.

`pyproject.toml`:

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Example project"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=9.0.0"
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

The important part:

```toml
pythonpath = ["."]
```

This tells pytest:

> "Look in the current directory when importing modules."

Imports:

```python
from src.utils import clamp
```

Structure:

```text
src/
├── __init__.py
└── utils.py
```

Advantages:

* Simple.
* Easy to understand.
* Great for learning Python.
* No packaging complexity.

Disadvantages:

* `src` becomes part of the import path.
* Not ideal for publishing a library.

---

# Option 2: Proper Python Package Layout

Used for professional projects and packages.

Structure:

```text
.
├── pyproject.toml
├── src
│   └── my_project
│       ├── __init__.py
│       └── utils.py
└── tests
```

Now `my_project` is the actual package.

`pyproject.toml` includes a build system:

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Example project"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=9.0.0"
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_project"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Imports:

```python
from my_project.utils import clamp
```

Now the package name is meaningful.

---

# Why the Proper Layout Is Preferred

Installing the project:

```bash
uv sync
```

or:

```bash
pip install .
```

makes your package available as:

```python
from my_project.utils import clamp
```

This is how external libraries work:

```python
from fastapi import FastAPI
from requests import get
from pandas import DataFrame
```

The user imports the package name, not the folder where the code happens to live.

---

# Rust Comparison

Simple Python:

```python
from src.utils import clamp
```

is similar to:

```rust
mod utils;
use utils::clamp;
```

Everything is local.

Proper Python package:

```python
from my_project.utils import clamp
```

is closer to:

```rust
use my_project::utils::clamp;
```

The crate/package has a real public name.

---

# Which Should I Use?

## Learning / small projects

Use:

```text
src/
    utils.py
```

with:

```python
from src.utils import clamp
```

and a simple `pyproject.toml`.

---

## Portfolio / production / PyPI

Use:

```text
src/
    my_project/
        utils.py
```

with a build system in `pyproject.toml`.

---

The main thing learned:

* `src` is just a directory convention.
* The inner folder (`my_project`) is the actual Python package.
* `pyproject.toml` can describe either a simple application or a distributable package.
* The "proper" layout scales better, but the simple version is perfectly valid for learning.

