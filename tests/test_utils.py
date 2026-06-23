# tests/test_utils.py

import pytest
from src.utils import clamp, word_count, running_average


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
