#!/usr/bin/env python3
"""
The drill loop — active recall over this lab, on a spaced-repetition schedule.

    python drill.py                      pick what is due (or weakest) and start
    python drill.py --topic quick_sort   drill one concept
    python drill.py --topic trees        drill something from a family
    python drill.py --check quick_sort   grade your attempt and reschedule it
    python drill.py --list               the schedule
    python drill.py --stats              how you are doing
    python drill.py --reveal quick_sort  show the reference (after you have tried)
    python drill.py --reset [slug]       forget one topic's history, or all of it

Reading an implementation feels like learning and mostly is not. Reproducing it
from the invariant is what moves it into memory, which is the only thing this
script exists to force.
"""

import argparse
import sys
from collections.abc import Sequence

import curriculum
from curriculum.schema import Topic
from drills import grade as grading
from drills import stubs
from drills.schedule import History

RULE = "-" * 72


def print_prompt(topic: Topic, show_hints: bool = True) -> None:
    """
    Show what you need to reconstruct the algorithm — and nothing more.

    Deliberately withheld: the code, the pitfalls, and the interview problems.
    Pitfalls are the answers to mistakes you have not made yet; reading them
    first turns recall back into recognition.
    """
    complexity = topic.complexity
    print(RULE)
    print(f"  {topic.name}   [{topic.family}]   slug: {topic.slug}")
    print(RULE)
    print()
    print("  INVARIANT — the thing to hold on to")
    for line in _wrap(topic.invariant):
        print(f"    {line}")
    print()
    print(f"  TARGET COMPLEXITY   {complexity.as_row()}   space {complexity.space}")
    flags = topic.flag_summary()
    if flags != "—":
        print(f"  PROPERTIES          {flags}")
    print()

    if show_hints:
        print("  MENTAL MODEL")
        for line in _wrap(topic.mental_model):
            print(f"    {line}")
        print()
        print("  REACH FOR IT WHEN")
        for line in _wrap(topic.use_when):
            print(f"    {line}")
        print()


def _wrap(text: str, width: int = 66) -> list[str]:
    words, lines, current = text.split(), [], ""
    for word in words:
        if current and len(current) + len(word) + 1 > width:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}" if current else word
    if current:
        lines.append(current)
    return lines


def select_topic(history: History, wanted: str | None) -> Topic | None:
    """
    Choose what to drill: an explicit request, else whatever is due.

    An unrecognised name is matched against families and slugs before giving up,
    so `--topic trees` and `--topic graph` both work.
    """
    if wanted:
        if wanted in curriculum.BY_SLUG:
            return curriculum.get(wanted)
        matches = curriculum.in_family(wanted)
        if not matches:
            print(f"No topic or family matches {wanted!r}.")
            print("Try `python drill.py --list` to see the slugs.")
            return None
        due = history.due_topics()
        for topic in due:
            if topic in matches:
                return topic
        return matches[0]

    due = history.due_topics()
    return due[0] if due else None


def command_drill(args, history: History) -> int:
    topic = select_topic(history, args.topic)
    if topic is None:
        print("Nothing is due. Pick one explicitly with --topic, or --list to browse.")
        return 0

    record = history.get(topic.slug)
    path, was_written = stubs.create_attempt(topic, overwrite=args.fresh)

    print()
    print_prompt(topic, show_hints=not args.no_hints)

    if record.attempts:
        accuracy = record.accuracy() or 0.0
        print(f"  HISTORY   {record.attempts} attempt(s), {accuracy:.0%} pass rate, "
              f"streak {record.streak}, last {record.last_result}")
        print()

    print(f"  YOUR FILE   {path.relative_to(stubs.REPO_ROOT)}")
    if not was_written:
        print("              (your existing attempt was kept — --fresh starts over)")
    else:
        print("              (fresh stub: every body raises NotImplementedError)")
    print()
    print("  Fill in every body, then:")
    print(f"      python drill.py --check {topic.slug}")
    print(RULE)
    return 0


def command_check(args, history: History) -> int:
    slug = args.check
    if slug not in curriculum.BY_SLUG:
        print(f"Unknown topic {slug!r}. Try `python drill.py --list`.")
        return 2

    topic = curriculum.get(slug)
    path = stubs.existing_attempt(slug)
    if path is None:
        print(f"No attempt found. Start one with `python drill.py --topic {slug}`.")
        return 2

    print()
    print(f"Grading {topic.name}...")
    result = grading.grade(topic, path)
    print(result.render())
    print()

    if not result.graded:
        print("  Recording this as a self-assessed attempt requires --pass or --fail.")
        if args.mark_pass or args.mark_fail:
            record = history.record_attempt(slug, passed=args.mark_pass, note="self-assessed")
            history.save()
            print(f"  Recorded as {record.last_result}. Next review: {record.next_due}.")
        return 0

    record = history.record_attempt(slug, passed=result.passed)
    history.save()

    print(f"  Next review: {record.next_due}  (streak {record.streak})")
    if result.passed:
        print()
        print("  Now read the pitfalls you did NOT hit — that is where the")
        print(f"  remaining value is:  head -60 {topic.path}")
    else:
        print()
        print(f"  Compare: python drill.py --reveal {slug}")
    print()
    return 0


def command_reveal(args, _history: History) -> int:
    slug = args.reveal
    if slug not in curriculum.BY_SLUG:
        print(f"Unknown topic {slug!r}.")
        return 2
    topic = curriculum.get(slug)
    path = stubs.existing_attempt(slug)

    if path is None:
        print(f"No attempt to compare against. The reference is {topic.path}.")
        return 0

    print()
    print(f"Diff of your attempt against {topic.path}:")
    print(RULE)
    print(grading.diff_against_reference(topic, path))
    print(RULE)
    return 0


def command_list(args, history: History) -> int:
    print()
    print(f"{'slug':34} {'family':26} {'due':>6}  attempts")
    print(RULE)
    for topic in curriculum.ALL_TOPICS:
        record = history.records.get(topic.slug)
        if record is None or record.is_new:
            due, attempts = "new", "-"
        else:
            days = record.days_until_due()
            due = "now" if days is not None and days <= 0 else f"{days}d"
            attempts = f"{record.passes}/{record.attempts}"
        if args.due_only and due not in {"new", "now"}:
            continue
        print(f"{topic.slug:34} {topic.family:26} {due:>6}  {attempts}")
    print()
    return 0


def command_stats(_args, history: History) -> int:
    summary = history.summary()
    print()
    print("  DRILL STATS")
    print(RULE)
    for label, value in summary.items():
        print(f"    {label.replace('_', ' '):16} {value}")

    weakest = history.weakest_topics(limit=8)
    if weakest:
        print()
        print("  WEAKEST (lowest pass rate)")
        for topic in weakest:
            record = history.get(topic.slug)
            print(f"    {topic.slug:32} {record.accuracy() or 0:.0%}  "
                  f"({record.passes}/{record.attempts})")
    print()
    return 0


def command_reset(args, history: History) -> int:
    slug = None if args.reset is True or args.reset == "all" else args.reset
    if slug and slug not in curriculum.BY_SLUG:
        print(f"Unknown topic {slug!r}.")
        return 2
    cleared = history.reset(slug)
    history.save()
    target = slug or "all topics"
    print(f"Cleared drill history for {target} ({cleared} record(s)).")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="drill.py",
        description="Spaced-repetition drilling over the dsa-lab curriculum.",
    )
    parser.add_argument("--topic", metavar="SLUG_OR_FAMILY", help="what to drill")
    parser.add_argument("--check", metavar="SLUG", help="grade an attempt and reschedule it")
    parser.add_argument("--reveal", metavar="SLUG", help="diff your attempt against the reference")
    parser.add_argument("--list", action="store_true", help="show the schedule")
    parser.add_argument("--due-only", action="store_true", help="with --list, hide what is not due")
    parser.add_argument("--stats", action="store_true", help="show progress")
    parser.add_argument("--reset", nargs="?", const=True, metavar="SLUG",
                        help="forget one topic's history, or all of it")
    parser.add_argument("--fresh", action="store_true", help="overwrite an existing attempt")
    parser.add_argument("--no-hints", action="store_true",
                        help="show only the invariant, not the mental model")
    parser.add_argument("--pass", dest="mark_pass", action="store_true",
                        help="self-assess an ungradable topic as passed")
    parser.add_argument("--fail", dest="mark_fail", action="store_true",
                        help="self-assess an ungradable topic as failed")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    history = History.load()

    if args.reset is not None:
        return command_reset(args, history)
    if args.stats:
        return command_stats(args, history)
    if args.list:
        return command_list(args, history)
    if args.reveal:
        return command_reveal(args, history)
    if args.check:
        return command_check(args, history)
    return command_drill(args, history)


if __name__ == "__main__":
    sys.exit(main())
