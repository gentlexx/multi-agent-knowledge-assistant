import ast
from pathlib import Path

import pytest

from src.tools import _evaluate_arithmetic, _safe_note_path


ROOT = Path(__file__).resolve().parents[1]


def test_all_python_files_parse():
    for path in [*ROOT.glob("*.py"), *ROOT.glob("src/*.py"), *ROOT.glob("tests/*.py")]:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


@pytest.mark.parametrize(
    ("expression", "expected"),
    [("1 + 2 * 3", 7), ("(8 - 2) / 3", 2), ("2 ** 8", 256)],
)
def test_safe_arithmetic(expression, expected):
    assert _evaluate_arithmetic(expression) == expected


@pytest.mark.parametrize("expression", ["__import__('os').system('whoami')", "open('x')", "a + 1"])
def test_arithmetic_rejects_code(expression):
    with pytest.raises(ValueError):
        _evaluate_arithmetic(expression)


def test_note_path_stays_in_notes_directory():
    assert _safe_note_path("demo.txt").name == "demo.txt"
    with pytest.raises(ValueError):
        _safe_note_path("../outside.txt")
