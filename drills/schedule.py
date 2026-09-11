"""
Spaced repetition state: what you have drilled, how it went, what is due.

Intervals expand on a pass and collapse to one day on a fail. The point is that
the schedule decides what to practise, not your mood — you will otherwise drill
quick sort for the fifth time and never touch Bellman-Ford.

History lives in a plain JSON file so it is readable, diffable and trivially
repairable by hand.
"""

import json
import pathlib
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta

import curriculum

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
HISTORY_PATH = REPO_ROOT / ".drill_history.json"

# Days until the next review after each consecutive pass. A sixth pass and
# beyond reuses the last value.
INTERVALS = (1, 3, 7, 16, 35, 90)
FAIL_INTERVAL_DAYS = 1
HISTORY_VERSION = 1


@dataclass
class Record:
    """One topic's drill history."""

    slug: str
    attempts: int = 0
    passes: int = 0
    fails: int = 0
    streak: int = 0
    last_attempt: str | None = None
    next_due: str | None = None
    last_result: str | None = None
    seconds_spent: float = 0.0
    notes: list[str] = field(default_factory=list)

    @property
    def is_new(self) -> bool:
        return self.attempts == 0

    def days_until_due(self, today: date | None = None) -> int | None:
        """Negative when overdue, None when never attempted."""
        if self.next_due is None:
            return None
        today = today or date.today()
        return (date.fromisoformat(self.next_due) - today).days

    def accuracy(self) -> float | None:
        return (self.passes / self.attempts) if self.attempts else None


class History:
    """The drill log, loaded from and saved to a single JSON file."""

    def __init__(self, records: dict[str, Record] | None = None) -> None:
        self.records: dict[str, Record] = records or {}

    @classmethod
    def load(cls, path: pathlib.Path = HISTORY_PATH) -> "History":
        """
        Read the history file, tolerating absence and corruption.

        A study tool that refuses to start because its progress file is malformed
        is worse than one that starts fresh, so a bad file is skipped rather than
        raised.
        """
        if not path.exists():
            return cls()
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return cls()

        records = {}
        for slug, payload in raw.get("records", {}).items():
            known = {f: payload.get(f) for f in Record.__dataclass_fields__ if f in payload}
            known["slug"] = slug
            known.setdefault("notes", [])
            records[slug] = Record(**known)
        return cls(records)

    def save(self, path: pathlib.Path = HISTORY_PATH) -> None:
        payload = {
            "version": HISTORY_VERSION,
            "updated": datetime.now().isoformat(timespec="seconds"),
            "records": {slug: asdict(record) for slug, record in sorted(self.records.items())},
        }
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def get(self, slug: str) -> Record:
        return self.records.setdefault(slug, Record(slug=slug))

    def record_attempt(
        self,
        slug: str,
        passed: bool,
        seconds: float = 0.0,
        note: str | None = None,
    ) -> Record:
        """
        Log one attempt and schedule the next review.

        A pass advances one step along INTERVALS; a fail resets the streak and
        brings the topic back tomorrow. Resetting rather than merely stepping back
        is deliberate: a topic you got wrong is a topic you do not know.
        """
        record = self.get(slug)
        record.attempts += 1
        record.seconds_spent += seconds
        record.last_attempt = date.today().isoformat()
        record.last_result = "pass" if passed else "fail"

        if passed:
            record.passes += 1
            record.streak += 1
            step = min(record.streak - 1, len(INTERVALS) - 1)
            gap = INTERVALS[step]
        else:
            record.fails += 1
            record.streak = 0
            gap = FAIL_INTERVAL_DAYS

        record.next_due = (date.today() + timedelta(days=gap)).isoformat()
        if note:
            record.notes.append(f"{record.last_attempt}: {note}")
        return record

    def reset(self, slug: str | None = None) -> int:
        """Forget one topic's history, or all of it. Returns how many were cleared."""
        if slug is None:
            cleared = len(self.records)
            self.records = {}
            return cleared
        return 1 if self.records.pop(slug, None) is not None else 0

    def due_topics(self, today: date | None = None) -> list[curriculum.Topic]:
        """
        Topics to practise now, most overdue first, then never-attempted ones.

        Sorting overdue before new means a topic you are actively forgetting wins
        over a topic you have never seen — forgetting is the more urgent problem.
        """
        today = today or date.today()
        overdue, unseen = [], []
        for topic in curriculum.ALL_TOPICS:
            record = self.records.get(topic.slug)
            if record is None or record.is_new:
                unseen.append(topic)
                continue
            days = record.days_until_due(today)
            if days is not None and days <= 0:
                overdue.append((days, topic))

        overdue.sort(key=lambda pair: pair[0])
        return [topic for _, topic in overdue] + unseen

    def weakest_topics(self, limit: int = 10) -> list[curriculum.Topic]:
        """
        Topics with the worst pass rate, attempted at least once.

        Separate from `due_topics` because 'what am I bad at' and 'what am I
        about to forget' are different questions.
        """
        scored = []
        for topic in curriculum.ALL_TOPICS:
            record = self.records.get(topic.slug)
            if record is None or record.is_new:
                continue
            scored.append((record.accuracy() or 0.0, -record.fails, topic))
        scored.sort(key=lambda item: (item[0], item[1]))
        return [topic for _, _, topic in scored[:limit]]

    def summary(self) -> dict[str, int]:
        """Counts for the stats view."""
        total = len(curriculum.ALL_TOPICS)
        attempted = sum(1 for r in self.records.values() if not r.is_new)
        due = len([t for t in self.due_topics() if not self.get(t.slug).is_new])
        return {
            "topics": total,
            "attempted": attempted,
            "untouched": total - attempted,
            "due_now": due,
            "total_attempts": sum(r.attempts for r in self.records.values()),
            "total_passes": sum(r.passes for r in self.records.values()),
            "total_fails": sum(r.fails for r in self.records.values()),
        }
