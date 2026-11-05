# Auditing the Isaac Sim skills as a content set

Before using any skill, I wanted to know what I was looking at. How many skills are there? Does the router cover them all? Do the skills share a structure? Would an agent be able to tell them apart?

The skills live in the `skills/` folder of the [isaac-sim/IsaacSim](https://github.com/isaac-sim/IsaacSim/tree/release/6.3/skills) repository. `SKILLS.md` in that folder is the router: the page an agent reads to decide which skill fits a request.

## Run the scripts yourself

```bash
git clone --depth 1 --branch release/6.3 --filter=blob:none --sparse \
  https://github.com/isaac-sim/IsaacSim.git
git -C IsaacSim sparse-checkout set skills
pip install pyyaml        # only the linter needs this

python3 scripts/router_coverage.py     IsaacSim/skills
python3 scripts/check_headers.py       IsaacSim/skills
python3 scripts/check_desc_lengths.py  IsaacSim/skills
python3 scripts/audit_skills_linter.py IsaacSim/skills
```

The output in [results/](results/) comes from `release/6.3` at commit `fcf16e4`.

## What the numbers say

**Coverage.** The router links all 44 skills ([results](results/router_coverage.txt)). Three skills appear in two routes: `isaac-sim-orchestrator`, `isaac-sim-troubleshooting` and `isaac-sim-validator`.

**Structure.** A census of every H2 heading ([results](results/check_headers.txt)) shows four near-universal headings:

| Heading | Share of skills |
| --- | --- |
| Purpose | 100% |
| Limitations | 97.7% |
| Troubleshooting | 97.7% |
| Prerequisites | 95.5% |
| Running scripts | 70.5% |
| Available Scripts | 65.9% |
| Workflow | 27.3% |

After those, the headings fragment. Some differ only in casing, such as "Related skills" and "Related Skills". Five different headings all mean "when to use this skill". The census points to a standard SKILL.md template, which I sketch below.

**Agent-facing quality.** An agent keeps every skill's description in context while choosing a skill, so descriptions matter more than body text for routing.

- All 44 descriptions fit within the 1,024-character limit. The longest is 334 characters, for `isaac-sim-assets` ([results](results/check_desc_lengths.txt)).
- 21 of 44 skills never say what they should *not* be used for. A "don't use this for" line helps an agent avoid picking the wrong skill ([results](results/audit_skills_linter.txt)).
- Two pairs of skills have heavily overlapping descriptions: `generate-incident-config` with `run-incident-events`, and `navigation-primitives` with `occupancy-map`. Overlap like that can confuse an agent choosing between them.

**Open questions.** I couldn't find evals for the skills. There's also no audience level, so nothing marks a skill as beginner or advanced, and nothing says where a newcomer should start.

## How far to trust these numbers

- The counts come from the scripts, and anyone can rerun them.
- The linter's thresholds are starting points, not standards. The 20-skill soft cap is a rule of thumb. The six-shared-keywords collision threshold has not been tuned.
- The negative-boundary check searches for phrases such as "do not use" and "not for". A skill could state its limits in other words and still be counted as missing them.
- I used Gemini for a first pass at grouping heading synonyms. I treated the grouping as a suggestion to check against the counts, not as a finding.

## A proposed SKILL.md skeleton

Built from the heading census. The comments say which existing headings each section would absorb.

```markdown
## Purpose
<!-- In 100% of skills today -->

## When to use
<!-- Absorbs: "When to use this skill", "When to use (vs siblings)", "I want to… → use this" -->
<!-- Include a "Don't use this for" line -->

## Prerequisites
<!-- In 95.5%: environment, NGC tags, dependencies, hardware -->

## Available scripts

## Running scripts

## Workflow

## Related skills
<!-- Absorbs: "Related Skills", "Read These Skills First", "Integration points" -->

## Limitations
<!-- Absorbs: "Safety rules", "Boundaries" -->

## Troubleshooting

## Verify it worked
<!-- Absorbs: "Validation Checklist" -->
```

## Turning this into a docs-health check

Each check above is cheap, repeatable and specific about what to fix, so each one could run in CI on every change to `skills/`. A dashboard would track the same numbers over time: router coverage, template conformance, descriptions without a negative boundary, and overlapping pairs. I haven't built that dashboard. These scripts are the first step towards one.
