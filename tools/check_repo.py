"""Checks that run on every push to this repo.

1. Every relative link in a Markdown file points at a file or folder that exists.
2. Every Python script compiles.
3. No real IPv4 address appears in the docs. Use placeholders such as
   <PUBLIC_IP>. Loopback, 0.0.0.0 and the documented 100.64.0.0/10 range
   are allowed.

Usage: python3 tools/check_repo.py
Exit code 1 if any check fails.
"""
import ipaddress
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {".git"}
ALLOWED_IPS = {"127.0.0.1", "0.0.0.0", "100.64.0.0"}
LINK = re.compile(r"\]\(([^)\s]+)\)")
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def files(pattern):
    return [p for p in ROOT.rglob(pattern) if not SKIP & set(p.relative_to(ROOT).parts)]


def check_links():
    errors = []
    for md in files("*.md"):
        for target in LINK.findall(md.read_text(encoding="utf-8")):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            path = target.split("#")[0]
            if path and not (md.parent / path).exists():
                errors.append(f"{md.relative_to(ROOT)}: broken link {target}")
    return errors


def check_python():
    errors = []
    for py in files("*.py"):
        try:
            compile(py.read_text(encoding="utf-8"), str(py), "exec")
        except SyntaxError as exc:
            errors.append(f"{py.relative_to(ROOT)}:{exc.lineno}: {exc.msg}")
    return errors


def check_ips():
    errors = []
    for f in files("*.md") + files("*.yml") + files("*.txt"):
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for ip in IPV4.findall(line):
                try:
                    ipaddress.IPv4Address(ip)
                except ValueError:
                    continue
                if ip not in ALLOWED_IPS:
                    errors.append(f"{f.relative_to(ROOT)}:{n}: real IP address {ip}, use a placeholder")
    return errors


def main():
    failed = False
    for name, check in [("links", check_links), ("python", check_python), ("ip addresses", check_ips)]:
        errors = check()
        print(f"{'FAIL' if errors else 'PASS'}  {name}")
        for e in errors:
            print(f"      {e}")
        failed |= bool(errors)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
