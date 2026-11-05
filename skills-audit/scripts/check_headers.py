"""Count how often each H2 heading appears across SKILL.md files.

A heading that appears in nearly every skill is a de facto standard. A long
tail of near-duplicates ("Related skills" and "Related Skills") shows where a
template would help.

Usage: python3 check_headers.py <path-to-skills-folder>
"""
import re
import sys
from collections import Counter
from pathlib import Path


def main(skills_dir: Path) -> None:
    headers_by_skill = {}
    all_h2 = Counter()
    for d in sorted(p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith(".")):
        f = d / "SKILL.md"
        if f.is_file():
            h2s = [h.strip() for h in re.findall(r"^##\s+(.+)$", f.read_text(errors="ignore"), re.M)]
            headers_by_skill[d.name] = h2s
            all_h2.update(h2s)

    total = len(headers_by_skill)
    print(f"Total skills: {total}\n")
    print(f"{'H2 Header':<40} | {'Count':<5} | {'%':<6}")
    print("-" * 55)
    for h, c in all_h2.most_common():
        pct = (c / total * 100) if total else 0
        print(f"{h:<40} | {c:<5} | {pct:>5.1f}%")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(Path(sys.argv[1]))
