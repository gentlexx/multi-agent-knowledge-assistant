"""Fail when common secrets, local paths, or oversized files enter the repository."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache"}
MAX_FILE_SIZE = 5 * 1024 * 1024
PATTERNS = {
    "OpenAI-style key": re.compile(r"sk-[A-Za-z0-9]{20,}"),
    "Chinese phone number": re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    "Windows user path": re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
    "local project path": re.compile(r"D:\\AI_learning", re.IGNORECASE),
}


def iter_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and not any(part in SKIP_PARTS for part in path.parts):
            yield path


def main() -> int:
    findings = []
    for path in iter_files():
        relative = path.relative_to(ROOT)
        if path.stat().st_size > MAX_FILE_SIZE:
            findings.append(f"oversized file: {relative}")
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(content):
                findings.append(f"{label}: {relative}")

    if findings:
        print("Repository audit failed:")
        for finding in sorted(set(findings)):
            print(f"- {finding}")
        return 1

    print("Repository audit passed: no blocked patterns or files over 5 MiB.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
