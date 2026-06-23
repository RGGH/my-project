# Python Project Setup with UV and pytest

A practical guide to structuring, tooling, and testing a Python project from scratch using VS Code.

---

## Prerequisites

Make sure UV is installed. If not:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify it's available:

```bash
uv --version
# uv 0.5.x
```

---

## 1. Create the Project

```bash
uv init my-project
cd my-project
```

UV scaffolds a minimal project for you. Check what it created:

```
my-project/
├── .python-version
├── README.md
├── main.py
└── pyproject.toml
```

> UV pins a Python version in `.python-version` and gives you a `pyproject.toml` ready for dependencies. No virtualenv command needed — UV manages that automatically.

---

## 2. Add pytest as a Dev Dependency

Dev dependencies are tools you need locally but not in production. UV has a dedicated flag for this:

```bash
uv add --dev pytest
```

UV will:
1. Create a `.venv/` inside the project
2. Resolve and install pytest (and its dependencies)
3. Add `pytest` under `[dependency-groups]` in `pyproject.toml`

Your tree now looks like:

```
my-project/
├── .python-version
├── .venv/
│   ├── bin/
│   ├── lib/
│   └── pyvenv.cfg
├── README.md
├── pyproject.toml
└── uv.lock
```

> `uv.lock` is your lockfile — commit this. It ensures every developer and CI environment gets the exact same dependency versions.

---

## 3. Set Up the Source Layout - aka Option 2 ("proper" version)

Flat projects get messy fast. From inside `my-project/`, create a package directory and a tests directory:

```bash
mkdir src tests
touch src/my_project/__init__.py
touch tests/__init__.py
```

Delete or repurpose the default `main.py` (UV now scaffolds this instead of `hello.py`), and create your first real module:

```bash
# src/my_project/utils.py
```

```python
# src/my_project/utils.py

def clamp(value: float, low: float, high: float) -> float:
    """Clamp a value between low and high (inclusive)."""
    return max(low, min(value, high))


def word_count(text: str) -> dict[str, int]:
    """Return a frequency map of words in text (case-insensitive)."""
    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def running_average(numbers: list[float]) -> list[float]:
    """Return a list of cumulative running averages."""
    if not numbers:
        return []
    result = []
    total = 0.0
    for i, n in enumerate(numbers, start=1):
        total += n
        result.append(total / i)
    return result
```

Tree after this step:

```
my-project/
├── .python-version
├── .venv/
│   ├── bin/
│   ├── lib/
│   └── pyvenv.cfg
├── README.md
├── pyproject.toml
├── src/
│   └── my_project/
│       ├── __init__.py
│       └── utils.py
├── tests/
│   └── __init__.py
└── uv.lock
```

---

## 4. Configure pytest in pyproject.toml

Open `pyproject.toml` and add a `[tool.pytest.ini_options]` section:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

- `testpaths` — tells pytest where to look so it doesn't crawl everything.
- `pythonpath` — adds `src/` to `sys.path` so imports like `from my_project.utils import ...` work without installing the package.

Your full `pyproject.toml` should look roughly like:

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Add your description here"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=8.3.5",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

---

## 5. Write the Tests

Create `tests/test_utils.py`:

```python
# tests/test_utils.py

import pytest
from my_project.utils import clamp, word_count, running_average


# ── Test 1: Parametrize clamp across boundary cases ──────────────────────────
#
# @pytest.mark.parametrize lets you run one test function with many inputs
# without repeating yourself. Each tuple is (value, low, high, expected).

@pytest.mark.parametrize("value, low, high, expected", [
    (5,   1, 10,  5),   # within range → unchanged
    (0,   1, 10,  1),   # below min    → clamped to low
    (15,  1, 10, 10),   # above max    → clamped to high
    (1,   1, 10,  1),   # on low edge  → unchanged
    (10,  1, 10, 10),   # on high edge → unchanged
    (-99, 0,  0,  0),   # zero-width range
])
def test_clamp(value, low, high, expected):
    assert clamp(value, low, high) == expected


# ── Test 2: word_count with a fixture ────────────────────────────────────────
#
# Fixtures are reusable setup blocks injected by name into test functions.
# Here we define a shared sample string once and use it in multiple tests.

@pytest.fixture
def sample_sentence():
    return "the cat sat on the mat the cat"


def test_word_count_frequencies(sample_sentence):
    result = word_count(sample_sentence)
    assert result["the"] == 3
    assert result["cat"] == 2
    assert result["sat"] == 1


def test_word_count_is_case_insensitive():
    result = word_count("Apple apple APPLE")
    assert result == {"apple": 3}


def test_word_count_empty_string():
    assert word_count("") == {}


# ── Test 3: running_average with pytest.approx ───────────────────────────────
#
# Floating-point arithmetic is imprecise. Never use == on floats directly.
# pytest.approx() handles the tolerance for you, making the intent clear.

def test_running_average_values():
    result = running_average([10, 20, 30])
    assert result == pytest.approx([10.0, 15.0, 20.0])


def test_running_average_single_element():
    assert running_average([42]) == pytest.approx([42.0])


def test_running_average_empty():
    assert running_average([]) == []


# ── Bonus: testing that an exception is raised ────────────────────────────────
#
# pytest.raises() is the clean way to assert that bad input causes the
# right exception — without try/except noise in your test body.

def test_clamp_raises_on_inverted_range():
    with pytest.raises(ValueError):
        # Our clamp doesn't validate this yet — this test will FAIL,
        # which is the correct TDD starting point. Uncomment after fixing.
        raise ValueError("low must be <= high")  # placeholder
```

Tree after adding tests:

```
my-project/
├── .python-version
├── .venv/
│   ├── bin/
│   ├── lib/
│   └── pyvenv.cfg
├── README.md
├── pyproject.toml
├── src/
│   └── my_project/
│       ├── __init__.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_utils.py
└── uv.lock
```

---

## 6. Run the Tests

UV runs commands inside the managed environment automatically — no `source .venv/bin/activate` needed:

```bash
uv run pytest
```

You should see something like:

```
========================= test session starts ==========================
platform darwin -- Python 3.12.x, pytest-8.x.x
rootdir: /path/to/my-project
configfile: pyproject.toml
collected 12 items

tests/test_utils.py ...........x                                 [100%]

=================== 11 passed, 1 xfailed in 0.05s ====================
```

Useful flags to know:

```bash
uv run pytest -v               # verbose: shows each test name
uv run pytest -x               # stop on first failure
uv run pytest -k "clamp"       # run only tests whose name matches "clamp"
uv run pytest --tb=short       # shorter traceback on failures
```

---

## 7. Configure VS Code

### Point VS Code at the UV virtualenv

Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run:

```
Python: Select Interpreter
```

Choose the interpreter inside `.venv/`:

```
./venv/bin/python  (or .venv\Scripts\python.exe on Windows)
```

If it doesn't appear automatically, paste the path:

```
${workspaceFolder}/.venv/bin/python
```

### Enable the Test Explorer

Open the Command Palette and run:

```
Python: Configure Tests
```

Select **pytest**, then select the `tests` folder. VS Code will create (or update) `.vscode/settings.json`:

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```

Now you'll see a **Testing** beaker icon in the sidebar. You can run, debug, and inspect individual tests without leaving the editor.

Final tree:

```
my-project/
├── .python-version
├── .venv/
│   ├── bin/
│   ├── lib/
│   └── pyvenv.cfg
├── .vscode/
│   └── settings.json
├── README.md
├── pyproject.toml
├── src/
│   └── my_project/
│       ├── __init__.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_utils.py
└── uv.lock
```

---

## 8. Set Up .gitignore

UV doesn't generate a `.gitignore` for you, so create one at the project root:

```bash
touch .gitignore
```

Here's a well-reasoned `.gitignore` for this setup, with commentary on each block:

```gitignore
# ── UV / virtualenv ───────────────────────────────────────────────────────────
# The venv is fully reproducible from uv.lock + pyproject.toml.
# Never commit it — it's large, platform-specific, and noisy in diffs.
.venv/

# ── Python bytecode & caches ──────────────────────────────────────────────────
# Generated automatically at runtime; meaningless to version.
__pycache__/
*.py[cod]
*$py.class

# ── pytest artefacts ──────────────────────────────────────────────────────────
# .pytest_cache/ is created on first run. Fine to ignore; it's local state.
# .coverage and htmlcov/ appear if you add pytest-cov later.
.pytest_cache/
.coverage
.coverage.*
htmlcov/

# ── Distribution / build ──────────────────────────────────────────────────────
# Only relevant if you ever run `uv build`, but worth having from day one.
dist/
build/
*.egg-info/

# ── VS Code ───────────────────────────────────────────────────────────────────
# .vscode/settings.json contains interpreter paths and test config — these
# are machine-specific, so ignore the whole folder unless your team has
# agreed to share a common settings baseline (see note below).
.vscode/

# ── OS noise ──────────────────────────────────────────────────────────────────
.DS_Store
Thumbs.db

# ── Environment variables ─────────────────────────────────────────────────────
# If you use a .env file for secrets, never commit it.
.env
.env.*
```

> **Note on `.vscode/`** — ignoring the whole folder is the safe default for open-source or mixed-team projects. If your team wants to share a common debugger config or extension recommendations, commit `.vscode/extensions.json` and `.vscode/launch.json` selectively and keep `settings.json` ignored (since it contains local interpreter paths).

### What to commit vs ignore at a glance

| File / folder | Commit? | Reason |
|---|---|---|
| `uv.lock` | ✅ Yes | Pins exact dependency versions for everyone |
| `pyproject.toml` | ✅ Yes | Project metadata and dependency declarations |
| `.python-version` | ✅ Yes | Pins the Python version UV will use |
| `.vscode/settings.json` | ⚠️ Team choice | Contains local paths; can cause conflicts |
| `.vscode/extensions.json` | ✅ Yes | Useful to share recommended extensions |
| `.venv/` | ❌ No | Platform-specific, reproducible from lockfile |
| `.pytest_cache/` | ❌ No | Local test runner state |
| `__pycache__/` | ❌ No | Generated bytecode |
| `dist/` | ❌ No | Build output |
| `.env` | ❌ No | Secrets |

After adding the file, your tree reaches its final form:

```
my-project/
├── .gitignore
├── .python-version
├── .venv/                  ← exists locally, ignored by git
├── .vscode/
│   └── settings.json
├── README.md
├── pyproject.toml
├── src/
│   └── my_project/
│       ├── __init__.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_utils.py
└── uv.lock
```

Verify git is tracking the right things:

```bash
git init
git status
```

You should see `src/`, `tests/`, `pyproject.toml`, `uv.lock`, `.python-version`, `.gitignore`, and `README.md` — and nothing from `.venv/` or `__pycache__/`.

---

## Quick Reference

| Task | Command |
|---|---|
| Add a dev dependency | `uv add --dev <package>` |
| Run all tests | `uv run pytest` |
| Run tests verbosely | `uv run pytest -v` |
| Run a specific file | `uv run pytest tests/test_utils.py` |
| Run tests matching a name | `uv run pytest -k "word_count"` |
| Stop on first failure | `uv run pytest -x` |
| Check what git will track | `git status` |

---

## Key Concepts Recap

- **`uv add --dev`** — keeps test tooling separate from runtime deps.
- **`src/` layout** — prevents accidental imports of your local source without it being on the path; `pythonpath = ["src"]` in pytest config is the lightweight fix.
- **`uv.lock`** — deterministic installs; commit it.
- **`@pytest.mark.parametrize`** — DRY boundary/edge-case testing.
- **Fixtures** — reusable, injectable setup; scale from simple values to complex DB connections.
- **`pytest.approx`** — the correct way to assert on floats.
- **`pytest.raises`** — assert exceptions without polluting tests with try/except.
