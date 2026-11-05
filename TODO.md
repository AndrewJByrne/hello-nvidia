# Open work: tests, evals, reproductions and a built skill

This repo shows work in progress. Each item says why it matters.

## The audit scripts have no tests, and two checks are weak

- [ ] **Add tests.** Build a small fixture folder of fake skills with known answers (a missing router link, a duplicate route, an over-long description, a missing boundary) and check that each script reports exactly those answers. Today the only evidence that the scripts are right is that their output matched my manual reading.
- [ ] **Fix the argument check.** The linter looks for parameters declared in frontmatter. No Isaac Sim skill declares any, so the check can't fail on these skills.
- [ ] **Narrow the boundary check to the description.** The check searches each skill's whole file for phrases like "do not use", but agents choose a skill from its description. The 21-of-44 number may change after the fix.
- [ ] **Source or tune the thresholds.** The 20-skill cap, the 5-argument maximum and the six-shared-keywords overlap are rules of thumb. Only the 1,024-character limit comes from the Agent Skills format. Thresholds should be agreed with the team and checked against real routing results.
- [ ] **Check overlap against behaviour, not just words.** Two descriptions sharing keywords doesn't prove an agent confuses them. A routing eval (below) would show whether the flagged pairs are real problems.
- [ ] **Pin dependencies.** The linter needs PyYAML, and no version is pinned.
- [ ] **Run the audit on a schedule.** A CI job could rerun the scripts against the latest `skills/` and show the trend, which is the start of a docs-health dashboard.

## `hello-isaac-sim` is a spec, so it needs building, evals and a timed run

- [ ] **Build the skill.** Today the skill is a [spec](hello-isaac-sim/SPEC.md), not working code.
- [ ] **Write evals.** Two kinds:
  - *Routing evals:* newcomer prompts ("I'm on a cloud GPU, show me Isaac Sim") should route to `hello-isaac-sim`, and unrelated prompts should not.
  - *Outcome evals:* the spec's seven done criteria, run on a fresh Brev machine by a tester who hasn't seen the skill.
- [ ] **Time a fresh run, with and without the skill.** I haven't timed a repeat run, so I can't yet say how much the skill saves.
- [ ] **Propose the address fix upstream.** The IsaacSim contribution policy only accepts outside changes under `source/extensions/`, so the route is a GitHub Discussion, not a pull request.

## Two Brev findings need reproducing, and one setup is all I've tested

- [ ] **Reproduce two Brev CLI findings** (`--min-disk` ignored, `brev copy` copying nothing) on a fresh machine. I saw each only once.
- [ ] **Add the compose override files.** `docker-compose.public-ip.yml` and `docker-compose.python-server.yml` are still only on the Brev machine. The cheatsheet describes them, but the files themselves belong here.
- [ ] **Record a short video** of the Jetbot driving, so the result can be shown without a running machine.
- [ ] **Try a second demo,** such as a figure-eight, to see how far the skills go beyond driving forward.
- [ ] **Widen the test.** Everything here comes from one setup: one laptop, Chrome, and AWS through Brev. Other clouds and browsers are untested.
- [ ] **Send the findings to the right places.** The skills findings go to an IsaacSim GitHub Discussion. The Brev CLI findings go to Brev support.

## The human-docs notes may be out of date

- [ ] **Recheck the notes against the current docs.** The notes are one person's first impressions on one day, and the docs may have changed since.

## The repo has no license and few CI checks

- [ ] **Add more checks to CI.** The checks today cover relative links, Python syntax and stray IP addresses. External links, Markdown style and spelling aren't checked.
- [ ] **Add a license.** The repo has none yet.
