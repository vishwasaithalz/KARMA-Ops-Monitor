#!/usr/bin/env python3
"""Refresh a public-only GitHub CI signal board. No private repositories or secret values."""
from __future__ import annotations
import datetime
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

OWNER = "vishwasaithalz"
PROJECTS = [
    ("LogSentry", "LogSentry", "Tests"),
    ("Recon Lite", "recon-lite", "Tests"),
    ("AI Automation Lab", "AI-Automation-Lab", "Tests"),
    ("CyberPlayground", "CyberPlayground", "Tests"),
    ("YinYangYoHackers", "YYYH", "CI"),
    ("Flagship API", "flagship-api", "Tests"),
    ("Next.js Starter", "nextjs-boilerplate", "CI"),
    ("GitHub Profile", "vishwasaithalz", "Profile quality"),
]
OUT = Path(__file__).resolve().parents[1] / "public-status.json"

def fetch(repo: str):
    url = f"https://api.github.com/repos/{OWNER}/{repo}/actions/runs?branch=main&per_page=30"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "KARMA-Ops-Monitor-Public-Status",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.load(response)
        return data.get("workflow_runs", []), None
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return [], exc.__class__.__name__

def main():
    captured = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    entries = []
    for display_name, repo, workflow in PROJECTS:
        runs, error = fetch(repo)
        selected = next((r for r in runs if r.get("name") == workflow and r.get("head_branch") == "main"), None)
        state = "unavailable" if error else "not_verified"
        item = {
            "name": display_name,
            "repository": repo,
            "workflow": workflow,
            "state": state,
            "run_url": None,
            "run_at": None,
        }
        if selected:
            status = selected.get("status")
            conclusion = selected.get("conclusion")
            if status == "completed" and conclusion == "success":
                item["state"] = "passed"
            elif status == "completed":
                item["state"] = "failed"
            else:
                item["state"] = "running"
            item["run_url"] = selected.get("html_url")
            item["run_at"] = selected.get("created_at")
        entries.append(item)
        print(f"{display_name}: {item['state']}")
    assert sum(e["state"] != "unavailable" for e in entries) >= 1, "All public GitHub API requests failed"
    payload = {
        "generated_at_utc": captured,
        "data_policy": "Public GitHub Actions runs only. No secrets or private repository information.",
        "warning": "A green workflow result does not certify production, security or every application feature.",
        "projects": entries,
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Published {len(entries)} public projects to {OUT}")

if __name__ == "__main__":
    main()
