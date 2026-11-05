# Auditing the Isaac Sim skills as a content set

Before using any skill, I wanted to know what I was looking at. How many skills are there? Does the router cover them all? Do the skills share a structure? Would an agent be able to tell them apart?

The skills live in the `skills/` folder of the [isaac-sim/IsaacSim](https://github.com/isaac-sim/IsaacSim/tree/release/6.3/skills) repository. `SKILLS.md` in that folder is the router: the page an agent reads to decide which skill fits a request.

## How the scripts were made

I didn't write these scripts by hand. I worked with an AI agent (Gemini): I asked the questions above, the agent wrote the code, and I ran the scripts against the skills and checked the output. For this repo, the scripts were tidied to take the skills folder as an argument, and each one got a header that says what it checks.

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

**Structure.** I counted how many skills use each H2 heading ([results](results/check_headers.txt)). Four headings appear in almost every skill, at 95% or more. Three more appear in between a quarter and three quarters of the skills:

| Heading | Share of skills |
| --- | --- |
| Purpose | 100% |
| Limitations | 97.7% |
| Troubleshooting | 97.7% |
| Prerequisites | 95.5% |
| Running scripts | 70.5% |
| Available Scripts | 65.9% |
| Workflow | 27.3% |

Below those seven, the headings scatter. Some differ only in casing, such as "Related skills" and "Related Skills". Five different headings all mean "when to use this skill". The counts point to a shared SKILL.md template, which I sketch below.

**Agent-facing quality.** An agent keeps every skill's description in context while choosing a skill, so descriptions probably matter most when an agent picks a skill.

- All 44 descriptions fit within the 1,024-character limit. The longest is 334 characters, for `isaac-sim-assets` ([results](results/check_desc_lengths.txt)).
- 21 of 44 skills don't say what they should *not* be used for. A "don't use this for" line helps an agent avoid picking the wrong skill ([results](results/audit_skills_linter.txt)).
- Two pairs of skills share many description keywords: `generate-incident-config` with `run-incident-events`, and `navigation-primitives` with `occupancy-map`. Overlap like that may confuse an agent choosing between them.

**Open questions.** I didn't find evals for the skills in the `skills/` folder, though I didn't search everywhere they might live. I also didn't see a way to mark a skill as beginner or advanced, or a pointer to where a newcomer should start. Both may exist in places I didn't look.

## How far to trust these numbers

- The counts come from the scripts, and you can rerun them with the commands above.
- The linter's thresholds are starting points, not standards. The 20-skill soft cap is a rule of thumb. The six-shared-keywords collision threshold has not been tuned.
- The negative-boundary check searches for phrases such as "do not use" and "not for". A skill could state its limits in other words and still be counted as missing them.
- I also used Gemini for a first pass at grouping heading synonyms. I treated the grouping as a suggestion to check against the counts, not as a finding.
- The linter's argument check can't fail on these skills. The check looks for parameters declared in frontmatter, and no skill declares any.
- The negative-boundary check searches each skill's whole file, not just the description that agents use to choose a skill.

## One way to make the skills consistent: a SKILL.md template

This is one way I might approach consistency: a shared template, built from the heading counts above. The comments say which existing headings each section would absorb.

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
