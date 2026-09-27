#!/usr/bin/env python3
"""Download every add-on listed in entries.json from this repo's releases, for the catalog workflow.

Each entry's pak must be the asset <id>.pak of the release <id>-v<version> in this repository (not a draft).
Entries may not point anywhere else: no "url", "pak", "thumb_url" or "thumb_path" keys (the catalog's download
links and thumbnails are always this repo's). Needs the GitHub CLI (gh) and GITHUB_REPOSITORY.

  scripts/fetch-paks.py [entries.json] [paks dir]
"""
import json, os, re, subprocess, sys

ID = re.compile(r"^[a-z0-9][a-z0-9_-]{0,31}$")        # the agent's rule (it becomes <id>.pak)
VERSION = re.compile(r"^[0-9A-Za-z][0-9A-Za-z._-]{0,31}$")
THUMB = re.compile(r"^[A-Za-z0-9_-]{1,64}\.(png|jpg|jpeg)$")
FORBIDDEN = ("url", "pak", "thumb_url", "thumb_path")


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "entries.json"
    out = sys.argv[2] if len(sys.argv) > 2 else "paks"
    repo = os.environ["GITHUB_REPOSITORY"]
    entries = json.load(open(src)).get("addons", [])
    os.makedirs(out, exist_ok=True)
    bad = 0
    for e in entries:
        aid, ver = e.get("id", ""), e.get("version", "")
        why = None
        if not ID.match(aid): why = "id must be [a-z0-9][a-z0-9_-]*, at most 32 characters"
        elif not VERSION.match(ver): why = "version is required (letters, digits, . _ -)"
        elif any(k in e for k in FORBIDDEN): why = f"remove {', '.join(k for k in FORBIDDEN if k in e)}: paks and thumbnails come from this repo"
        elif e.get("thumb") and not (THUMB.match(e["thumb"]) and os.path.isfile(os.path.join("thumbs", e["thumb"]))):
            why = f"thumbnail thumbs/{e['thumb']} missing (png or jpg)"
        if why:
            print(f"::error::{aid or '?'}: {why}")
            bad += 1
            continue
        tag = f"{aid}-v{ver}"
        r = subprocess.run(["gh", "release", "view", tag, "-R", repo, "--json", "isDraft,assets"], capture_output=True, text=True)
        if r.returncode:
            print(f"::error::{aid}: no release {tag} in {repo} ({r.stderr.strip()})")
            bad += 1
            continue
        rel = json.loads(r.stdout)
        if rel["isDraft"] or f"{aid}.pak" not in [a["name"] for a in rel["assets"]]:
            print(f"::error::{aid}: release {tag} must be published and carry {aid}.pak")
            bad += 1
            continue
        subprocess.run(["gh", "release", "download", tag, "-R", repo, "-p", f"{aid}.pak", "-D", out, "--clobber"], check=True)
        print(f"{aid}: {tag}/{aid}.pak, {os.path.getsize(os.path.join(out, aid + '.pak'))} bytes")
    print(f"{len(entries) - bad} of {len(entries)} add-on(s) fetched")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
