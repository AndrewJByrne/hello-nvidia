"""A small linter for a set of agent skills.

Six checks, each reported as PASS, INFO, WARN or FAIL:
  1. Skill count against a soft cap. The cap of 20 is a rule of thumb,
     not an NVIDIA or industry standard.
  2. Description length against the 1,024-character limit in the
     Agent Skills format.
  3. Argument complexity, for skills that declare parameters in frontmatter.
  4. Volatile data (dates, user paths, session ids) in descriptions.
  5. Whether each skill says what it should NOT be used for.
  6. Pairs of skills whose descriptions share many keywords, which can
     confuse an agent choosing between them.

The keyword-overlap threshold (6 shared words) is a starting point to tune,
not a validated number.

Usage: python3 audit_skills_linter.py <path-to-skills-folder>
Requires: PyYAML
"""
import re
import sys
from pathlib import Path

import yaml


SOFT_SKILL_CAP = 20
DESC_CHAR_BUDGET = 1024
MAX_ARGS = 5

skills = []
if len(sys.argv) != 2:
    sys.exit(__doc__)
base_path = Path(sys.argv[1])

# 1. Collect skills and frontmatter/schemas
for d in sorted(p for p in base_path.iterdir() if p.is_dir() and not p.name.startswith(".")):
    f = d / "SKILL.md"
    if not f.is_file():
        continue
    
    txt = f.read_text(encoding="utf-8", errors="ignore")
    fm_match = re.match(r"^---\s*\n(.*?)\n---", txt, re.DOTALL)
    
    data = {}
    if fm_match:
        try:
            data = yaml.safe_load(fm_match.group(1)) or {}
        except Exception:
            data = {"raw_frontmatter": fm_match.group(1)}
            
    desc = data.get("description", "")
    if not desc and "raw_frontmatter" in data:
        # Fallback regex for unstructured YAML
        m = re.search(r"^description:\s*(.*?)(?=\n[a-zA-Z0-9_-]+:|\Z)", data["raw_frontmatter"], re.DOTALL | re.M)
        if m:
            desc = re.sub(r"^(?:>-|>|\|-|\|)\s*", "", m.group(1).strip()).strip("\"'")

    skills.append({
        "name": d.name,
        "path": f,
        "content": txt,
        "desc": str(desc),
        "data": data
    })

print(f"\n================ SKILL SUITE AUDIT REPORT ================\n")

# ----------------------------------------------------------------------
# Rule 1: Maximum Skills per System Check
# ----------------------------------------------------------------------
total_skills = len(skills)
print(f"[*] Total Skills Detected: {total_skills}")
if total_skills > SOFT_SKILL_CAP:
    print(f"  [WARN] {total_skills} skills found. Exceeds soft cap ({SOFT_SKILL_CAP}).")
    print(f"         The cap is a rule of thumb. Consider grouping skills behind routers.\n")
else:
    print(f"  [PASS] Within recommended single-agent capacity (< {SOFT_SKILL_CAP}).\n")

# ----------------------------------------------------------------------
# Rule 2: Token Budget & Description Size
# ----------------------------------------------------------------------
print(f"[*] Description Length & Token Budget Check (Cap: {DESC_CHAR_BUDGET} chars):")
over_budget = [s for s in skills if len(s["desc"]) > DESC_CHAR_BUDGET]
missing_desc = [s for s in skills if len(s["desc"]) == 0]

if over_budget:
    print(f"  [FAIL] {len(over_budget)} skills exceed the {DESC_CHAR_BUDGET}-character budget:")
    for s in over_budget:
        print(f"         - {s['name']}: {len(s['desc'])} chars (+{len(s['desc']) - DESC_CHAR_BUDGET})")
else:
    print(f"  [PASS] All skill descriptions within the {DESC_CHAR_BUDGET}-character limit.")

if missing_desc:
    print(f"  [WARN] {len(missing_desc)} skills are missing a frontmatter description:")
    for s in missing_desc:
        print(f"         - {s['name']}")
print()

# ----------------------------------------------------------------------
# Rule 3: Argument Complexity Ceilings
# ----------------------------------------------------------------------
print(f"[*] Argument Complexity Check (Max {MAX_ARGS} required properties):")
heavy_args = []
for s in skills:
    # Check parameters/args defined in frontmatter (JSON Schema style)
    props = {}
    required = []
    
    # Common schema keys used in tool definitions
    params = s["data"].get("parameters") or s["data"].get("inputs") or s["data"].get("arguments") or {}
    if isinstance(params, dict):
        props = params.get("properties", {})
        required = params.get("required", [])
        
    num_req = len(required) if required else len(props)
    if num_req > MAX_ARGS:
        heavy_args.append((s["name"], num_req))

if heavy_args:
    print(f"  [WARN] {len(heavy_args)} skills exceed {MAX_ARGS} properties:")
    for name, count in heavy_args:
        print(f"         - {name}: {count} properties")
else:
    print(f"  [PASS] No skills exceed argument complexity ceilings (or defined externally).")
print()

# ----------------------------------------------------------------------
# Rule 4: Dynamic Data Leaks in Descriptions
# ----------------------------------------------------------------------
print(f"[*] Dynamic / Volatile Data Leaks in Descriptions:")
dynamic_patterns = [
    (r"\b\d{4}-\d{2}-\d{2}\b", "Hardcoded Date (YYYY-MM-DD)"),
    (r"\b(session[_-]?id|user[_-]?id|auth_token)\s*[:=]\s*\S+", "Hardcoded Session/User Identity"),
    (r"(/home/\w+|/Users/\w+|C:\\Users\\\w+)", "Hardcoded Absolute User Path"),
]

dynamic_leaks = []
for s in skills:
    for pattern, label in dynamic_patterns:
        match = re.search(pattern, s["desc"], re.IGNORECASE)
        if match:
            dynamic_leaks.append((s["name"], label, match.group(0)))

if dynamic_leaks:
    print(f"  [WARN] Found {len(dynamic_leaks)} instances of volatile/system data in descriptions:")
    for name, label, snippet in dynamic_leaks:
        print(f"         - {name}: {label} -> '{snippet}'")
else:
    print(f"  [PASS] Descriptions appear static and free of runtime session data.")
print()

# ----------------------------------------------------------------------
# Rule 5: Negative / Exclusionary Phrasing
# ----------------------------------------------------------------------
print(f"[*] Exclusionary Phrasing Boundary Check:")
exclusion_cues = ["do not use", "not for", "cannot", "does not handle", "never use", "ignores", "exclusive of"]
missing_exclusions = []

for s in skills:
    has_exclusion = any(cue in s["desc"].lower() or cue in s["content"].lower() for cue in exclusion_cues)
    if not has_exclusion:
        missing_exclusions.append(s["name"])

if missing_exclusions:
    print(f"  [INFO] {len(missing_exclusions)}/{total_skills} skills lack explicit negative boundaries ('DO NOT use for...'):")
    print(f"         (Consider adding negative criteria to prevent false triggers, e.g., in {', '.join(missing_exclusions[:5])}...)")
else:
    print(f"  [PASS] All skills contain clear negative boundary definitions.")
print()

# ----------------------------------------------------------------------
# Rule 6: Overlapping Triggers & Routing Ambiguity
# ----------------------------------------------------------------------
print(f"[*] Potential Trigger & Scope Collision Matrix:")
# Tokenize descriptions into content keywords
stopwords = {"this", "that", "with", "from", "when", "into", "skill", "using", "uses", "provides", "used"}
skill_keywords = {}
for s in skills:
    words = set(re.findall(r"[a-zA-Z]{4,}", s["desc"].lower())) - stopwords
    skill_keywords[s["name"]] = words

collisions = []
names = list(skill_keywords.keys())
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        k1, k2 = names[i], names[j]
        intersection = skill_keywords[k1] & skill_keywords[k2]
        # Flag if overlap is high relative to length
        if len(intersection) >= 6:
            collisions.append((k1, k2, intersection))

if collisions:
    print(f"  [WARN] Detected {len(collisions)} pairs with high description keyword overlap:")
    for k1, k2, shared in collisions[:8]:
        sample = ", ".join(sorted(shared)[:5])
        print(f"         - {k1} <--> {k2}")
        print(f"           Shared: {sample}")
    if len(collisions) > 8:
        print(f"           (... and {len(collisions) - 8} more pairs)")
else:
    print(f"  [PASS] No severe keyword collisions detected.")

print(f"\n==========================================================\n")
