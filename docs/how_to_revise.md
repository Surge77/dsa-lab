# How to revise with this repo

The short version: **do not read the code**. Reproduce it from the invariant,
let the tests tell you whether you were right, and let the schedule decide what
to practise next.

```bash
python drill.py                # whatever is due
```

---

## Why reading does not work

Rereading `quick_sort.py` produces *recognition* — it looks familiar, you nod,
you feel competent. Recognition collapses under interview or exam pressure
because the only pathway you exercised was the reading one.

Reproducing it from a blank file exercises *retrieval*, which is the pathway you
actually need. It is uncomfortable, noticeably slower per algorithm, and several
times more durable per minute spent.

Everything in this repo before the drill system was recognition material. The
drill loop is the part that changes outcomes.

---

## The loop

```bash
python drill.py --topic quick_sort
```

You get the **invariant**, the target complexity, the properties, and a mental
model. You do *not* get the code, the pitfalls, or the interview problems —
pitfalls are answers to mistakes you have not made yet, and reading them first
turns recall back into recognition.

A stub appears at `drills/attempts/quick_sort.py` with every signature and
docstring preserved and every body replaced by `raise NotImplementedError`. The
contract, not the answer.

Fill it in. Then:

```bash
python drill.py --check quick_sort
```

Sorts and searches are graded by `Utils/contracts.py` — the **same** contract the
reference implementations face in CI. There is no weaker standard for your own
work. Data structures are graded by running the topic's real pytest file against
your module.

On a pass the interval expands: 1 → 3 → 7 → 16 → 35 → 90 days. On a fail it
collapses to tomorrow. A topic you got wrong is a topic you do not know.

Then, and only then, read the pitfalls:

```bash
head -60 Sorting/efficient/quick_sort.py
```

---

## Commands

| Command | What it does |
|---|---|
| `python drill.py` | most-overdue topic, else an unseen one |
| `python drill.py --topic quick_sort` | one concept by slug |
| `python drill.py --topic trees` | anything from a family |
| `python drill.py --no-hints` | invariant only — hardest mode |
| `python drill.py --fresh` | discard your attempt and restub |
| `python drill.py --check <slug>` | grade and reschedule |
| `python drill.py --reveal <slug>` | diff your attempt vs the reference |
| `python drill.py --list` | the whole schedule |
| `python drill.py --list --due-only` | just what needs work |
| `python drill.py --stats` | pass rates, weakest topics |
| `python drill.py --reset <slug>` | forget one topic's history |

---

## Choosing what to do with the time you have

**Five minutes.** `python drill.py --list --due-only` and look at the
invariants of what comes up. No code.

**Twenty minutes.** One full drill: prompt → implement → check → read pitfalls.

**An hour.** Three drills from *different* families. Interleaving beats blocking:
three sorts in a row lets you coast on the previous one's momentum.

**A week before an interview.** `python drill.py --stats` to find your weakest
topics, then work the `INTERVIEW` lines in those files' headers. Every concept
lists its real LeetCode problems.

**Refreshing something you once knew.** Read the invariant and the PITFALLS
section only. Skip the mental model. The pitfalls are where the non-obvious
content lives.

---

## When you are stuck on a blank file

In this order:

1. Re-read the invariant. Most implementations are derivable from it.
2. State the base case out loud. Empty input, one element.
3. Write the loop or recursion shape with the body left blank.
4. `python drill.py --reveal <slug>` and diff.

Step 4 is not failure — it is the point at which looking is actually useful,
because you now have a specific question rather than a vague one.

---

## Building intuition, not just recall

**Watch an algorithm work:**

```python
from Utils.trace import trace_sort, compare_sorts
from Sorting.simple.bubble_sort import bubble_sort

print(trace_sort(bubble_sort, [5, 1, 4, 2, 8]))
```

Prints every write with the array state after it. Seeing one pass spend four
comparisons to accomplish three swaps is what makes O(n²) mean something.

`compare_sorts([...], values)` puts comparison and write counts side by side —
the fastest way to see why selection sort exists despite being slow: it makes far
fewer *writes*.

**Prove the complexity:**

```bash
python -m Utils.complexity
```

Times each algorithm at doubling sizes and prints the ratio. ~2 is linear,
~2.1–2.3 is n log n, ~4 is quadratic. Theory, then measurement, then belief.

---

## Finding things

[INDEX.md](../INDEX.md) has one row per concept with the complexity, the
properties, and a **"reach for it when"** column. That last column is the one
worth reading during revision: complexity tells you what something costs, that
column tells you why you would ever pick it.

The bottom of INDEX.md has a cross-reference map. Following those links beats
reading rows top to bottom, because the links are where the transferable ideas
are — `quick_sort → intro_sort` and `counting_sort → radix_sort` each carry one
real insight.

---

## Adding a concept

One place: a `Topic` entry in `curriculum/sorting.py`, `searching.py`, or
`structures.py`. Then:

```bash
python -m Utils.sync
```

That regenerates INDEX.md and the teaching header at the top of the source file.
The drill prompts and the stub generator read the same record, so nothing can
drift out of step.

`Tests/test_curriculum.py` fails if an implementation file exists with no
curriculum entry, if a cross-reference is dangling, or if INDEX.md is stale.
That is what stops the index rotting — six algorithms in this repo were
previously invisible and untested because nothing enforced it.
