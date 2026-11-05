# hello-nvidia

This repo documents my first steps with Isaac Sim and its agent skills.

**My goal:** to learn how agent skills and AI agents can help a newcomer experience Isaac Sim for the first time, using only NVIDIA's published skills.

My approach had two steps:

1. **Know the landscape, so I could choose a skill.** Working with an AI agent (Gemini), I produced short Python scripts that check how the `SKILLS.md` router covers the 44 skills, count the H2 headings in every skill, measure the descriptions, and lint the set against agent-facing practices. The agent wrote the code. I decided what to measure, ran the scripts, and checked the results.
2. **Build.** I used the skills the way a newcomer would. My done test was Isaac Sim running on a Brev cloud GPU, streaming to my laptop's browser, with a robot visibly driving. I logged the friction points I hit along the way.

![A Jetbot driving in Isaac Sim, streamed to a laptop browser](brev-first-simulation/screenshots/jetbot-closeup.png)

## The folders follow the order of the work

| Folder | What you'll find |
| --- | --- |
| [skills-audit/](skills-audit/) | The audit scripts, their output against the `release/6.3` skills, and what the numbers say |
| [human-docs-notes/](human-docs-notes/) | First impressions of the human-facing docs, from installing Isaac Sim before I tried the skills |
| [brev-first-simulation/](brev-first-simulation/) | The full write-up: every step with why, the command and what happened, the three gaps I found, recommendations, and a 43-entry friction log |
| [tools/](tools/) | The checks that CI runs on this repo |
| [cheatsheets/](cheatsheets/) | Commands, ports and addresses on one page each |
| [hello-isaac-sim/](hello-isaac-sim/) | A one-page spec for a beginner skill, with done criteria and tests |

## Where to start: the summary of the Brev write-up

A good place to start is the [summary of the Brev write-up](brev-first-simulation/README.md#summary). The summary covers what I set out to do, what got in the way, and what I'd recommend.

## Tests, evals and a built skill are next

I ran out of time before I could add tests for the scripts, write evals for the skills or build `hello-isaac-sim`. These are important pieces of work, not afterthoughts, and they're what I'd like to do next. The full list, with the reason for each item, is in [TODO.md](TODO.md).

## A lightweight CI check shows the approach

The CI here is small, and meant only to show the approach. Every push runs [tools/check_repo.py](tools/check_repo.py) in GitHub Actions. The check fails if a relative link is broken, if a Python script doesn't compile, or if a real IP address slips into the docs. Addresses in the docs are placeholders such as `<PUBLIC_IP>`.

If I took the CI further, these are the steps I'd try next, roughly in this order:

1. Run tests for the audit scripts on every push, so a change to a script can't quietly change the numbers.
2. Add an automated style check, so the writing rules a team agrees on are checked on every change. Add spelling and external link checks too.
3. Run the audit scripts against the upstream `skills/` folder on a schedule, and keep each run's results. Over time, the results would show trends, which is the start of a docs-health dashboard.
4. For skills, run routing and outcome evals whenever a skill changes, so a change is checked against how agents actually use the skill. Change management matters here, and a skill's pull request is one natural place for the evals to hook into the review.
