"""
Generate a blank-slate stub from a reference implementation.

Stubs are generated on demand from the real file rather than kept as a parallel
tree of 63 hand-written copies. That means they can never drift out of sync with
the code they mirror, and adding a topic costs nothing.

The signatures and docstrings survive; every body is replaced with
`raise NotImplementedError`. You get the contract, not the answer.
"""

import ast
import pathlib

import curriculum

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
ATTEMPTS_DIR = REPO_ROOT / "drills" / "attempts"

# The three node kinds that can carry a docstring and a signature.
DocNode = ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef

BANNER = """\
# Your attempt at: {name}
#
# Fill in every body below, then grade it with:
#     python drill.py --check {slug}
#
# Reference (do not open until you have tried): {path}
# Invariant to hold on to:
{invariant}
"""


def _indent_comment(text: str, width: int = 72) -> str:
    """Wrap `text` as a comment block."""
    words, lines, current = text.split(), [], "#   "
    for word in words:
        if len(current) + len(word) + 1 > width and current.strip() != "#":
            lines.append(current)
            current = f"#   {word}"
        else:
            current = f"{current} {word}" if current.strip() != "#" else f"#   {word}"
    if current.strip() != "#":
        lines.append(current)
    return "\n".join(lines)


def _signature(node: DocNode) -> str:
    """Render a def/class header line from its AST node."""
    if isinstance(node, ast.ClassDef):
        bases = ", ".join(ast.unparse(b) for b in node.bases)
        return f"class {node.name}({bases}):" if bases else f"class {node.name}:"

    assert isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    args = ast.unparse(node.args)
    returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    return f"{prefix} {node.name}({args}){returns}:"




def _docstring_block(node: DocNode, indent: str) -> list[str]:
    """The node's docstring, re-indented, or nothing if it has none."""
    doc = ast.get_docstring(node, clean=True)
    if not doc:
        return []
    lines = [f'{indent}"""']
    lines += [f"{indent}{line}".rstrip() for line in doc.splitlines()]
    lines.append(f'{indent}"""')
    return lines


def _stub_body(node: DocNode, indent: str) -> list[str]:
    """Docstring plus a NotImplementedError placeholder."""
    return [*_docstring_block(node, indent), f"{indent}raise NotImplementedError"]


def _stub_class(node: ast.ClassDef) -> list[str]:
    """A class shell with every method stubbed."""
    lines = [_signature(node), *_docstring_block(node, "    ")]
    methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    if not methods:
        lines.append("    raise NotImplementedError")
        return lines
    for method in methods:
        lines.append("")
        lines.append(f"    {_signature(method)}")
        lines += _stub_body(method, "        ")
    return lines


def render_stub(topic: curriculum.Topic) -> str:
    """
    Build the full stub file text for `topic`.

    Module-level constants are kept as-is: re-deriving a gap sequence or a shrink
    factor from memory tests nothing useful.
    """
    source = (REPO_ROOT / topic.path).read_text(encoding="utf-8")
    tree = ast.parse(source)

    parts = [
        BANNER.format(
            name=topic.name,
            slug=topic.slug,
            path=topic.path,
            invariant=_indent_comment(topic.invariant),
        )
    ]

    imports, constants, bodies = [], [], []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            constants.append(ast.unparse(node))
        elif isinstance(node, ast.ClassDef):
            bodies.append("\n".join(_stub_class(node)))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            bodies.append("\n".join([_signature(node), *_stub_body(node, "    ")]))

    if imports:
        parts.append("\n".join(imports))
    if constants:
        parts.append("\n".join(constants))
    parts.extend(bodies)

    return "\n\n\n".join(parts) + "\n"


def attempt_path(slug: str) -> pathlib.Path:
    return ATTEMPTS_DIR / f"{slug}.py"


def create_attempt(
    topic: curriculum.Topic, overwrite: bool = False
) -> tuple[pathlib.Path, bool]:
    """
    Write a stub for `topic`. Returns (path, was_written).

    Refuses to overwrite existing work unless asked: losing a half-finished
    attempt to an accidental re-run would be the fastest way to stop using this.
    The `was_written` flag lets the CLI say whether it kept your old attempt
    rather than guessing either way.
    """
    ATTEMPTS_DIR.mkdir(parents=True, exist_ok=True)
    init = ATTEMPTS_DIR / "__init__.py"
    if not init.exists():
        init.write_text('"""Your drill attempts. Untracked by git."""\n', encoding="utf-8")

    path = attempt_path(topic.slug)
    if path.exists() and not overwrite:
        return path, False
    path.write_text(render_stub(topic), encoding="utf-8")
    return path, True


def existing_attempt(slug: str) -> pathlib.Path | None:
    path = attempt_path(slug)
    return path if path.exists() else None
