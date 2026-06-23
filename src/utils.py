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
