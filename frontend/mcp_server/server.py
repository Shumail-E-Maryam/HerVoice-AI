import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
RESOURCE_FILE = BASE_DIR / "backend" / "knowledge" / "resources.json"


def load_resources():
    if not RESOURCE_FILE.exists():
        return []

    with open(
        RESOURCE_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def search_resources(query: str):
    query = query.lower()

    results = []

    for resource in load_resources():

        searchable = " ".join(
            [
                resource.get("title", ""),
                resource.get("content", ""),
                resource.get("country", ""),
                " ".join(resource.get("topics", [])),
                " ".join(resource.get("keywords", [])),
            ]
        ).lower()

        if any(
            word in searchable
            for word in query.split()
            if len(word) > 2
        ):
            results.append(
                {
                    "id": resource.get("id"),
                    "title": resource.get("title"),
                    "source": resource.get("source"),
                    "url": resource.get("url"),
                    "content": resource.get("content"),
                }
            )

    return results


def get_resource(resource_id: str):
    for resource in load_resources():

        if resource.get("id") == resource_id:
            return resource

    return None


def list_topics():

    topics = set()

    for resource in load_resources():
        topics.update(resource.get("topics", []))

    return sorted(topics)


if __name__ == "__main__":

    print("HerVoice Resource MCP Server")
    print("============================")
    print()

    print("Available operations:")
    print(" - search_resources(query)")
    print(" - get_resource(resource_id)")
    print(" - list_topics()")