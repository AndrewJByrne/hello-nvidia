# Skills audit cheatsheet

Each script takes the path to a `skills/` folder. See [skills-audit](../skills-audit/) for setup and results.

| Script | Question it answers |
| --- | --- |
| `router_coverage.py` | Does `SKILLS.md` link every skill? Which skills appear in more than one route? |
| `check_headers.py` | Which H2 headings do the skills share, and how fragmented is the long tail? |
| `check_desc_lengths.py` | How long is each description, measured against the 1,024-character limit? |
| `audit_skills_linter.py` | Skill count, description budget, volatile data, negative boundaries and overlapping descriptions |

Results on `release/6.3`: 44 skills, all routed. Three skills appear in two routes. All descriptions are within the limit. 21 of 44 skills have no "don't use this for" line. There are two overlapping pairs.
