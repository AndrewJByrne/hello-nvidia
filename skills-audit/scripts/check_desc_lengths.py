"""Measure each skill's frontmatter description.

An agent keeps every skill's description in context to decide which skill to
use, so descriptions have a budget. The Agent Skills format caps a
description at 1,024 characters.

Usage: python3 check_desc_lengths.py <path-to-skills-folder>
"""
import re
import sys
from pathlib import Path

BUDGET = 1024


def description(text: str) -> str:
    fm = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not fm:
        return ""
    m = re.search(r"^description:\s*(.*?)(?=\n[a-zA-Z0-9_-]+:|\Z)", fm.group(1), re.DOTALL | re.M)
    if not m:
        return ""
    return re.sub(r"^(?:>-|>|\|-|\|)\s*", "", m.group(1).strip()).strip("\"'")


def main(skills_dir: Path) -> None:
    results = []
    for d in sorted(p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith(".")):
        f = d / "SKILL.md"
        if f.is_file():
            results.append((d.name, len(description(f.read_text(encoding="utf-8", errors="ignore")))))

    print(f"{'Skill Name':<42} | {'Chars':<6} | Status")
    print("-" * 62)
    over = 0
    for name, count in sorted(results, key=lambda x: -x[1]):
        if count == 0:
            status = "MISSING"
        elif count > BUDGET:
            status = f"OVER (+{count - BUDGET})"
            over += 1
        else:
            status = "OK"
        print(f"{name:<42} | {count:<6} | {status}")
    print("-" * 62)
    print(f"Total: {len(results)} | Over {BUDGET} chars: {over}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(Path(sys.argv[1]))
