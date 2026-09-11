"""
The curriculum registry — the single source of truth for the lab.

Everything pedagogical is generated from these Topic records:

    INDEX.md                  <- Utils/sync.py
    teaching headers in code  <- Utils/sync.py
    drill prompts             <- drill.py
    coverage enforcement      <- Tests/test_curriculum.py

So the index cannot go stale and a file's header cannot contradict the index.
Add a concept in one of the family modules and it appears in all four places.
"""

from curriculum.schema import Complexity, Topic
from curriculum.searching import SEARCHING_TOPICS
from curriculum.sorting import SORTING_TOPICS
from curriculum.structures import STRUCTURE_TOPICS

__all__ = [
    "Complexity",
    "Topic",
    "ALL_TOPICS",
    "BY_SLUG",
    "families",
    "get",
    "in_family",
    "slugs",
]

ALL_TOPICS: list[Topic] = [*STRUCTURE_TOPICS, *SORTING_TOPICS, *SEARCHING_TOPICS]

BY_SLUG: dict[str, Topic] = {t.slug: t for t in ALL_TOPICS}

if len(BY_SLUG) != len(ALL_TOPICS):
    seen: set = set()
    duplicates = sorted({t.slug for t in ALL_TOPICS if t.slug in seen or seen.add(t.slug)})
    raise ValueError(f"duplicate topic slugs in curriculum: {duplicates}")


def get(slug: str) -> Topic:
    """Look up a topic by slug, with a helpful message when it is missing."""
    try:
        return BY_SLUG[slug]
    except KeyError:
        near = [s for s in BY_SLUG if slug in s or s in slug]
        hint = f" Did you mean: {', '.join(sorted(near))}?" if near else ""
        raise KeyError(f"unknown topic '{slug}'.{hint}") from None


def slugs() -> list[str]:
    """Every topic slug, in curriculum order."""
    return [t.slug for t in ALL_TOPICS]


def families() -> list[str]:
    """Distinct family names, in curriculum order."""
    ordered: list[str] = []
    for topic in ALL_TOPICS:
        if topic.family not in ordered:
            ordered.append(topic.family)
    return ordered


def in_family(needle: str) -> list[Topic]:
    """
    Topics whose family contains `needle`, case-insensitively.

    Lets `drill.py --topic trees` match "Structures / trees" without the caller
    knowing the exact family string.
    """
    lowered = needle.lower()
    return [t for t in ALL_TOPICS if lowered in t.family.lower() or lowered in t.slug]
