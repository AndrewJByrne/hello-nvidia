"""Check how the SKILLS.md router covers the skills.

Answers three questions about a skills folder:
  1. How many skills does the folder hold?
  2. Does the SKILLS.md router link every one of them?
  3. Which skills does the router link from more than one route?

Usage: python3 router_coverage.py <path-to-skills-folder>
"""
import re
import sys
from collections import Counter
from pathlib import Path

LINK = re.compile(r"\[(?:[^\]]*)\]\(([^)]+\.md(?:#[^)]*)?)\)")


def main(skills_dir: Path) -> None:
    skills = sorted(d.name for d in skills_dir.iterdir() if (d / "SKILL.md").is_file())
    router = (skills_dir / "SKILLS.md").read_text(encoding="utf-8", errors="ignore")

    links = [link.split("#")[0] for link in LINK.findall(router)]
    linked = {link.split("/")[0] for link in links if link.endswith("SKILL.md")}
    counts = Counter(links)

    print(f"Skills (folders with a SKILL.md): {len(skills)}")
    print(f"Skills linked from SKILLS.md:     {len(linked & set(skills))}")
    missing = sorted(set(skills) - linked)
    print(f"Skills not linked from SKILLS.md: {len(missing)}")
    for name in missing:
        print(f"  - {name}")
    print("\nLinked from more than one route:")
    for link, n in sorted(counts.items()):
        if n > 1:
            print(f"  {n} {link}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(Path(sys.argv[1]))
