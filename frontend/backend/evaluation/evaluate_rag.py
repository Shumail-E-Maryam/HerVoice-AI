import sys
from pathlib import Path

# Add backend root to Python's import path
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from knowledge.retriever import retrieve_knowledge


TEST_CASES = [
    ("Hello", False),
    (
        "What is Pakistan Ministry of Human Rights 1099?",
        True,
    ),
]


def main():
    passed = 0

    for query, should_find in TEST_CASES:
        results = retrieve_knowledge(
            query,
            limit=3,
        )

        found = len(results) > 0
        status = found == should_find

        if status:
            passed += 1

        print(
            f"{'PASS' if status else 'FAIL'} | {query}"
        )

    print()
    print(
        f"RAG retrieval evaluation: "
        f"{passed}/{len(TEST_CASES)} passed"
    )

    return 0 if passed == len(TEST_CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())