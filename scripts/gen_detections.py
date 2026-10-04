"""Generate the Detections section from rorywag/KQL-Detections at build time.

Run by the mkdocs-gen-files plugin. Pages are created in memory only; nothing
is written into docs/. The source repo is cloned into .cache/kql-detections
(gitignored), or updated with a fast-forward pull if the clone already exists.

Environment variables:
    KQL_DETECTIONS_DIR      use a different clone location
    KQL_DETECTIONS_OFFLINE  set to 1 to skip the pull and use the existing clone

Everything read from the clone is treated as untrusted. Header metadata is HTML-
and Markdown-escaped before it reaches a page (see md_text and plain_text), only
http(s) URLs become links, tactics are checked against the ATT&CK list, and
symlinks or paths that resolve outside the clone are never read.
"""

from __future__ import annotations

import html
import logging
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote

import mkdocs_gen_files
import yaml

REPO_URL = "https://github.com/rorywag/KQL-Detections"
SECTION = "detections"
ROOT = Path(__file__).resolve().parent.parent
CLONE_DIR = Path(os.environ.get("KQL_DETECTIONS_DIR", ROOT / ".cache" / "kql-detections"))

# INFO level on purpose: a WARNING would fail `mkdocs build --strict`.
log = logging.getLogger("mkdocs.plugins.gen_detections")

KNOWN_FIELDS = {
    "name": "name",
    "author": "author",
    "date": "date",
    "description": "description",
    "reference": "references",
    "references": "references",
    "tactic": "tactics",
    "tactics": "tactics",
    "technique": "techniques",
    "techniques": "techniques",
    "note": "notes",
    "notes": "notes",
}
# Fields whose value can carry on over following "//" lines.
MULTILINE_FIELDS = {"description", "notes"}

HEADER_FIELD_RE = re.compile(r"^//\s*([A-Za-z][A-Za-z ]{0,30}?)\s*:\s?(.*)$")
TITLE_CASE_KEY_RE = re.compile(r"^[A-Z][A-Za-z]*(?: [A-Z][A-Za-z]*)?$")
TECHNIQUE_ID_RE = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")
URL_RE = re.compile(r"https?://[^\s,<>]+[^\s,<>.)]")
LET_DYNAMIC_RE = re.compile(r"\blet\s+(\w+)\s*=\s*dynamic\(\s*\[(.*?)\]\s*\)", re.S)
STRING_RE = re.compile(r"'([^']*)'|\"([^\"]*)\"")

# Enterprise ATT&CK tactics in kill-chain order, taken from the matrix's tactic
# order in MITRE's ATT&CK v19 STIX data. v19 split Defense Evasion into Stealth and
# Defense Impairment; the old name is kept in its original slot because existing
# detection headers still use it. Tactics not listed here sort after these, A to Z.
TACTIC_ORDER = [
    "Reconnaissance",
    "Resource Development",
    "Initial Access",
    "Execution",
    "Persistence",
    "Privilege Escalation",
    "Defense Evasion",
    "Stealth",
    "Defense Impairment",
    "Credential Access",
    "Discovery",
    "Lateral Movement",
    "Collection",
    "Command and Control",
    "Exfiltration",
    "Impact",
]
UNMAPPED = "Unmapped"
KNOWN_TACTICS = {t.lower(): t for t in TACTIC_ORDER}


@dataclass
class Detection:
    source: Path
    rel_path: str
    slug: str = ""
    name: str = ""
    author: str = ""
    date: str = ""
    description: str = ""
    references: list[str] = field(default_factory=list)
    tactics: list[str] = field(default_factory=list)
    techniques: str = ""
    notes: list[str] = field(default_factory=list)
    extras: dict[str, str] = field(default_factory=dict)
    query: str = ""
    created: str = ""
    updated: str = ""


# --- Source repo --------------------------------------------------------------


def sync_repo() -> str:
    """Clone or update the source repo and return its checked-out branch name."""
    if (CLONE_DIR / ".git").is_dir():
        if not os.environ.get("KQL_DETECTIONS_OFFLINE"):
            result = subprocess.run(
                ["git", "-C", str(CLONE_DIR), "pull", "--ff-only", "--quiet"],
                capture_output=True, text=True, timeout=120,
            )
            if result.returncode:
                log.info("Could not update %s, using the existing clone: %s",
                         CLONE_DIR, result.stderr.strip())
    else:
        CLONE_DIR.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            # Full history (the repo is small): page dates come from git log.
            # core.symlinks=false checks symlinks out as plain files holding the
            # target path, so they can't point outside the clone.
            ["git", "clone", "--quiet", "-c", "core.symlinks=false", f"{REPO_URL}.git", str(CLONE_DIR)],
            check=True, timeout=300,
        )
    return subprocess.run(
        ["git", "-C", str(CLONE_DIR), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def git_dates(rel_path: str) -> tuple[str, str]:
    """First and last commit times of a file in the source repo, as "YYYY-MM-DD HH:MM" UTC."""
    result = subprocess.run(
        ["git", "-C", str(CLONE_DIR), "log", "--follow", "--format=%ad",
         "--date=format-local:%Y-%m-%d %H:%M", "--", rel_path],
        capture_output=True, text=True, env={**os.environ, "TZ": "UTC"},
    )
    stamps = result.stdout.split("\n")
    stamps = [s for s in stamps if s]
    return (stamps[-1], stamps[0]) if stamps else ("", "")


def is_safe_file(path: Path, root: Path) -> bool:
    """A regular file inside the clone: no symlink anywhere on its path within the
    clone, and its resolved location is still under the clone directory."""
    rel = path.relative_to(root)
    parts = root
    for part in rel.parts:
        parts = parts / part
        if parts.is_symlink():
            return False
    return path.is_file() and path.resolve().is_relative_to(root.resolve())


def read_text(path: Path, root: Path) -> str:
    if not is_safe_file(path, root):
        raise ValueError(f"refusing to read {path}: symlink or outside {root}")
    return path.read_text(encoding="utf-8", errors="replace")


def find_detection_files(root: Path) -> list[Path]:
    """Every .kql file, plus extensionless files that start with a // Name: header.
    Symlinks, and anything that resolves outside the clone, are skipped."""
    found = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if not is_safe_file(path, root):
            if path.is_symlink():
                log.info("Skipping symlink in %s: %s", REPO_URL, rel.as_posix())
            continue
        if path.suffix.lower() == ".kql":
            found.append(path)
        elif path.suffix == "":
            first_line = read_text(path, root).split("\n", 1)[0]
            if re.match(r"^//\s*Name\s*:", first_line):
                found.append(path)
    return found


# --- Parsing -------------------------------------------------------------------


def parse_detection(path: Path, root: Path) -> Detection:
    det = Detection(source=path, rel_path=path.relative_to(root).as_posix())
    lines = read_text(path, root).splitlines()

    # The header is the run of leading "//" lines. A bare "//" separates groups of
    # fields. A comment line that isn't a field continues the previous multi-line
    # field; anywhere else it's the query's own first comment, so the header ends.
    current = None
    header_end = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("//"):
            break
        text = stripped[2:].strip()
        match = HEADER_FIELD_RE.match(stripped)
        key = match.group(1).strip() if match else ""
        if match and (key.lower() in KNOWN_FIELDS or TITLE_CASE_KEY_RE.match(key)):
            current = KNOWN_FIELDS.get(key.lower(), key)
            add_field(det, current, match.group(2).strip())
        elif not text:
            current = None
        elif current in MULTILINE_FIELDS:
            add_field(det, current, text, continuation=True)
        else:
            break
        header_end = i + 1

    det.query = "\n".join(lines[header_end:]).strip("\n")
    det.name = det.name or path.stem
    return det


def add_field(det: Detection, key: str, value: str, continuation: bool = False) -> None:
    if key == "description":
        det.description = f"{det.description} {value}".strip()
    elif key == "notes":
        if continuation and det.notes:
            det.notes[-1] = f"{det.notes[-1]} {value}"
        elif value:
            det.notes.append(value)
    elif key == "references":
        urls = URL_RE.findall(value)
        det.references.extend(urls or ([value] if value else []))
    elif key == "tactics":
        for tactic in (t.strip() for t in value.split(",") if t.strip()):
            known = KNOWN_TACTICS.get(tactic.lower())
            if known:
                det.tactics.append(known)
            else:
                log.info("Ignoring unknown tactic %r in %s", tactic, det.rel_path)
    elif key == "techniques":
        det.techniques = f"{det.techniques}, {value}".strip(", ") if det.techniques else value
    elif key in ("name", "author", "date"):
        setattr(det, key, value)
    elif value:
        det.extras[key] = value


def placeholder_lists(query: str) -> list[str]:
    """Names of `let x = dynamic([...])` lists that only hold placeholder values."""
    names = []
    for name, inner in LET_DYNAMIC_RE.findall(query):
        code = re.sub(r"//[^\n]*", "", inner)
        values = [a or b for a, b in STRING_RE.findall(code)]
        leftover = STRING_RE.sub("", code).replace(",", "").strip()
        if leftover:  # numbers, expressions: not a simple list of strings
            continue
        if not values or all(is_placeholder(v) for v in values):
            names.append(name)
    return names


def is_placeholder(value: str) -> bool:
    return bool(
        re.fullmatch(r"[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+", value)             # EXCLUSION_ITEM
        or re.fullmatch(r"[A-Za-z0-9]+Exclusions?", value)                 # SHA256HashExclusions
        or re.search(r"(?i)placeholder|changeme|replace[_ -]?me", value)
    )


# --- Rendering -----------------------------------------------------------------


# Characters that start Markdown links (and reference definitions), images and
# attribute lists ({ onclick=... } via attr_list), plus the backslash itself.
MD_SPECIALS_RE = re.compile(r"([\\\[\](){}!])")
# Inline code spans, matched the way Python-Markdown's backtick pattern does. Their
# contents are left as written: Markdown already renders them as literal text
# (HTML-escaped), and backslash escapes would show inside them. A span preceded by
# a backslash isn't treated as code here, so any mismatch only over-escapes.
CODE_SPAN_RE = re.compile(r"(?<!\\)(`+)(.+?)(?<!`)\1(?!`)")


def md_text(text: str) -> str:
    """Untrusted text for a Markdown body: outside code spans it's Markdown-escaped,
    then HTML-escaped, so it renders as plain text and can't create tags, links,
    images or attributes."""
    text = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", text)
    out, pos = [], 0
    for m in CODE_SPAN_RE.finditer(text):
        out.append(_escape_md(text[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(_escape_md(text[pos:]))
    return "".join(out)


def _escape_md(text: str) -> str:
    return html.escape(MD_SPECIALS_RE.sub(r"\\\1", text), quote=True)


def plain_text(text: str) -> str:
    """Untrusted text for front matter. Material prints page.meta.title and
    description into HTML without escaping, so they're HTML-escaped here."""
    text = re.sub(r"[\x00-\x1f\x7f]", " ", text)
    return html.escape(re.sub(r"\s+", " ", text).strip(), quote=True)


def mitre_url(technique_id: str) -> str:
    return f"https://attack.mitre.org/techniques/{technique_id.replace('.', '/')}/"


def link_techniques(text: str) -> str:
    return TECHNIQUE_ID_RE.sub(lambda m: f"[{m.group(0)}]({mitre_url(m.group(0))})", text)


def technique_ids(text: str) -> list[str]:
    return list(dict.fromkeys(TECHNIQUE_ID_RE.findall(text)))


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "detection"


def plain_description(det: Detection) -> str:
    """One plain-text line for front matter: the first sentence of Description, or Name."""
    text = re.sub(r"\s+", " ", det.description.replace("`", "")).strip()
    if not text:
        return f"KQL detection: {det.name}."
    sentence = re.split(r"(?<=[.!?])\s+", text)[0]
    if len(sentence) > 200:
        sentence = sentence[:197].rsplit(" ", 1)[0] + "..."
    return sentence


def front_matter(meta: dict) -> str:
    return "---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=1000) + "---\n\n"


def fenced(code: str, lang: str) -> str:
    longest = max((len(run) for run in re.findall(r"`+", code)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}{lang}\n{code}\n{fence}\n"


def cell(text: str) -> str:
    """Make text safe inside a markdown table cell."""
    return text.replace("|", "\\|").replace("\n", " ") or "-"


def indent(text: str) -> str:
    return "\n".join(f"    {line}" if line else "" for line in text.splitlines())


def is_http_url(ref: str) -> bool:
    return bool(re.fullmatch(r"https?://[^\s<>\"'`]+", ref))


def render_detection(det: Detection, branch: str) -> str:
    meta = {"title": plain_text(det.name), "description": plain_text(plain_description(det))}
    if det.tactics:
        meta["tags"] = det.tactics
    # Feed dates (see the rss plugin's date_from_meta in mkdocs.yml).
    if det.created:
        meta["date"] = det.created
    if det.updated:
        meta["updated"] = det.updated
    # Every header value below comes from the source repo: md_text() keeps it plain
    # text. Only http(s) references become links.
    out = [front_matter(meta), f"# {md_text(det.name)}\n\n"]

    if det.description:
        out.append(f"{md_text(det.description)}\n\n")

    cells = [cell(md_text(", ".join(det.tactics))), cell(link_techniques(md_text(det.techniques))),
             cell(md_text(det.author)), cell(md_text(det.date))]
    details = "| Tactic | Technique | Author | Date |\n|---|---|---|---|\n| " + " | ".join(cells) + " |\n"
    for key, value in det.extras.items():
        details += f"\n**{md_text(key)}:** {md_text(value)}\n"
    if det.references:
        details += "\n**References**\n\n" + "".join(
            f"- <{ref}>\n" if is_http_url(ref) else f"- {md_text(ref)}\n" for ref in det.references
        )
    out.append('!!! abstract "Detection details"\n\n' + indent(details) + "\n\n")

    if det.notes:
        out.append('!!! note "Notes"\n\n' + indent("".join(f"- {md_text(n)}\n" for n in det.notes)) + "\n\n")

    placeholders = placeholder_lists(det.query)
    if placeholders:
        names = ", ".join(f"`{n}`" for n in placeholders)
        out.append(
            '!!! warning "Placeholders to tune"\n\n'
            f"    {names} {'is a placeholder list' if len(placeholders) == 1 else 'are placeholder lists'}. "
            "Fill in known-good values from your environment before you deploy this query.\n\n"
        )

    out.append("## Query\n\n" + fenced(det.query, "kql") + "\n")
    source = f"{REPO_URL}/blob/{quote(branch)}/{quote(det.rel_path)}"
    out.append(f"[View source on GitHub]({source}){{ .md-button }}\n")
    return "".join(out)


def render_index(detections: list[Detection]) -> str:
    meta = {
        "title": "Detections",
        "description": "KQL detection queries for Microsoft Sentinel and Defender, "
                       "generated from the KQL-Detections repository.",
    }
    rows = []
    for det in sorted(detections, key=lambda d: d.name.lower()):
        ids = technique_ids(det.techniques)
        technique = ", ".join(f"[{i}]({mitre_url(i)})" for i in ids) or cell(md_text(det.techniques))
        rows.append(f"| [{cell(md_text(det.name))}]({det.slug}.md) | {cell(md_text(', '.join(det.tactics)))} | "
                    f"{technique} | {cell(md_text(det.date))} |")
    return (
        front_matter(meta)
        + "# Detections\n\n"
        + f"KQL detection queries from [rorywag/KQL-Detections]({REPO_URL}). "
        + "Browse them [by tactic](tactics.md) or use the table below.\n\n"
        + "| Name | Tactic | Technique | Date |\n|---|---|---|---|\n"
        + "\n".join(rows) + "\n"
    )


def render_tactics() -> str:
    meta = {"title": "By tactic", "description": "Detections grouped by MITRE ATT&CK tactic."}
    return front_matter(meta) + "# Detections by tactic\n\n<!-- material/tags -->\n"


def tactic_sort_key(tactic: str) -> tuple:
    known = {t.lower(): i for i, t in enumerate(TACTIC_ORDER)}
    if tactic == UNMAPPED:
        return (2, "")
    if tactic.lower() in known:
        return (0, known[tactic.lower()])
    return (1, tactic.lower())


def render_nav(detections: list[Detection]) -> str:
    """Overview, then one section per tactic in kill-chain order. A detection with
    several tactics is listed under each one, like the By tactic page."""
    by_tactic: dict[str, list[Detection]] = {}
    for det in detections:
        for tactic in det.tactics or [UNMAPPED]:
            by_tactic.setdefault(tactic, []).append(det)

    items = ["* [Overview](index.md)"]
    for tactic in sorted(by_tactic, key=tactic_sort_key):
        items.append(f"* {md_text(tactic)}")
        for det in sorted(by_tactic[tactic], key=lambda d: d.name.lower()):
            items.append(f"    * [{md_text(det.name)}]({det.slug}.md)")
    return "\n".join(items) + "\n"


# --- Main ----------------------------------------------------------------------


def main() -> None:
    branch = sync_repo()
    detections = [parse_detection(p, CLONE_DIR) for p in find_detection_files(CLONE_DIR)]

    used: set[str] = set()
    for det in detections:
        slug = base = slugify(Path(det.rel_path).stem)
        n = 2
        while slug in used or slug in ("index", "tactics"):
            slug, n = f"{base}-{n}", n + 1
        used.add(slug)
        det.slug = slug
        # Created: the Date header if it's a real date, else the file's first commit.
        first, last = git_dates(det.rel_path)
        det.created = f"{det.date} 00:00" if re.fullmatch(r"\d{4}-\d{2}-\d{2}", det.date) else first
        # The Date header is local time and commits are UTC, so a same-day edit can land
        # a few hours "before" creation. Never let updated precede created.
        det.updated = max(last, det.created)

    for det in detections:
        path = f"{SECTION}/{det.slug}.md"
        with mkdocs_gen_files.open(path, "w") as f:
            f.write(render_detection(det, branch))

    with mkdocs_gen_files.open(f"{SECTION}/index.md", "w") as f:
        f.write(render_index(detections))
    with mkdocs_gen_files.open(f"{SECTION}/tactics.md", "w") as f:
        f.write(render_tactics())
    with mkdocs_gen_files.open(f"{SECTION}/NAV.md", "w") as f:
        f.write(render_nav(detections))

    log.info("Generated %d detection pages from %s", len(detections), REPO_URL)


main()
