"""
The Topic record — one entry per concept in the lab.

This is the single source of truth for everything pedagogical. INDEX.md, the
teaching headers inside the implementation files, and the prompts that drill.py
shows you are all generated from these records, so they cannot drift apart.

Add a concept here and it appears everywhere. Tests/test_curriculum.py fails if
an implementation file exists with no Topic pointing at it, which is what stops
the index rotting as the lab grows.
"""

from dataclasses import dataclass, field

UNKNOWN = "—"


@dataclass(frozen=True)
class Complexity:
    """Asymptotic cost, written the way you would say it out loud."""

    best: str
    average: str
    worst: str
    space: str

    def as_row(self) -> str:
        if self.best == self.average == self.worst:
            return f"{self.best} (all cases)"
        return f"{self.best} / {self.average} / {self.worst}"


@dataclass(frozen=True)
class Topic:
    """
    One revisable concept.

    `slug` is the stable identifier used by drill.py and by cross-references in
    `see_also`, so renaming one means updating the references that point at it
    (Tests/test_curriculum.py catches dangling ones).
    """

    slug: str
    name: str
    family: str
    module: str
    entry: str
    mental_model: str
    invariant: str
    complexity: Complexity
    use_when: str
    avoid_when: str
    pitfalls: list[str] = field(default_factory=list)
    see_also: list[str] = field(default_factory=list)
    interview: list[str] = field(default_factory=list)
    doc: str | None = None

    # Dotted module paths that belong to this concept but are not its entry
    # point — e.g. a graph split across base/utils/algorithms files. Used by the
    # coverage test so helper modules do not each need their own Topic.
    also_covers: list[str] = field(default_factory=list)

    # Tri-state: True, False, or None where the question does not apply.
    stable: bool | None = None
    in_place: bool | None = None
    adaptive: bool | None = None

    @property
    def path(self) -> str:
        """Repository-relative path of the implementation file."""
        return self.module.replace(".", "/") + ".py"

    @property
    def all_paths(self) -> list[str]:
        """Every implementation file this Topic is responsible for."""
        return [self.path] + [m.replace(".", "/") + ".py" for m in self.also_covers]

    @property
    def is_sort(self) -> bool:
        return self.family.startswith("Sorting")

    @property
    def is_search(self) -> bool:
        return self.family.startswith("Searching")

    def flag_summary(self) -> str:
        """Short human-readable property line, omitting inapplicable flags."""

        def mark(label: str, value: bool | None) -> str | None:
            if value is None:
                return None
            return f"{label} {'yes' if value else 'no'}"

        parts = [
            mark("stable", self.stable),
            mark("in-place", self.in_place),
            mark("adaptive", self.adaptive),
        ]
        present = [p for p in parts if p]
        return "  ".join(present) if present else UNKNOWN
