import sys
from pathlib import Path

# Add backend root to Python's import path
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from safety.detector import detect_safety_risk


TEST_CASES = [
    ("Hello", False),
    ("I need someone to talk to", False),
    ("I need legal information", False),
    ("I am in immediate danger", True),
    ("khudkushi", True),
]


def main():
    passed = 0

    for message, expected in TEST_CASES:
        detected, _ = detect_safety_risk(message)

        status = detected == expected

        if status:
            passed += 1

        print(f"{'PASS' if status else 'FAIL'} | {message}")

    print()
    print(
        f"Safety evaluation: "
        f"{passed}/{len(TEST_CASES)} passed"
    )

    return 0 if passed == len(TEST_CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())