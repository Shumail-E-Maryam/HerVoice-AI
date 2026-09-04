import json
import re
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
KNOWLEDGE_FILE = BASE_DIR / "knowledge" / "resources.json"


def _load_resources() -> list[dict[str, Any]]:
    if not KNOWLEDGE_FILE.exists():
        return []

    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (OSError, json.JSONDecodeError):
        return []


def _tokens(text: str) -> set[str]:
    text = text.lower()

    return {
        token
        for token in re.findall(r"\b[\w'-]+\b", text)
        if len(token) > 2
    }


def _score(query: str, resource: dict[str, Any]) -> float:
    query_tokens = _tokens(query)

    if not query_tokens:
        return 0.0

    searchable_parts = [
        resource.get("title", ""),
        resource.get("content", ""),
        resource.get("country", ""),
        " ".join(resource.get("topics", [])),
        " ".join(resource.get("keywords", [])),
    ]

    resource_text = " ".join(searchable_parts).lower()
    resource_tokens = _tokens(resource_text)

    overlap = query_tokens.intersection(resource_tokens)

    score = len(overlap)

    query_lower = query.lower()

    title = resource.get("title", "").lower()

    if title and title in query_lower:
        score += 5

    for keyword in resource.get("keywords", []):
        if keyword.lower() in query_lower:
            score += 3

    return float(score)


def retrieve_knowledge(
    query: str,
    limit: int = 3,
) -> list[dict[str, Any]]:

    resources = _load_resources()

    if not resources:
        return []

    scored = []

    for resource in resources:
        score = _score(query, resource)

        if score > 0:
            scored.append((score, resource))

    scored.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        resource
        for _, resource in scored[:limit]
    ]


def format_knowledge_context(
    results: list[dict[str, Any]],
) -> str:

    if not results:
        return ""

    blocks = []

    for resource in results:

        title = resource.get("title", "Verified Resource")
        content = resource.get("content", "")
        source = resource.get("source", "")
        url = resource.get("url", "")

        blocks.append(
            f"TITLE: {title}\n"
            f"SOURCE: {source}\n"
            f"URL: {url}\n"
            f"CONTENT: {content}"
        )

    return "\n\n---\n\n".join(blocks)