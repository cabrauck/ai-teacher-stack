#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


LABELS_PATH = Path(__file__).resolve().parents[1] / ".github" / "labels.json"


@dataclass(frozen=True)
class Label:
    name: str
    color: str
    description: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync GitHub labels from .github/labels.json using gh."
    )
    parser.add_argument(
        "--repo",
        help="GitHub repository in owner/name form. Defaults to the current gh repository.",
    )
    parser.add_argument(
        "--labels",
        default=str(LABELS_PATH),
        help="Path to the label JSON file.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report required changes without creating or editing labels.",
    )
    return parser.parse_args()


def run_gh(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gh", *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def require_success(result: subprocess.CompletedProcess[str], action: str) -> None:
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"{action} failed: {message}")


def resolve_repo(repo: str | None) -> str:
    if repo:
        return repo

    result = run_gh(["repo", "view", "--json", "nameWithOwner"])
    require_success(result, "Resolving repository")
    data = json.loads(result.stdout)
    return data["nameWithOwner"]


def normalize_color(color: str) -> str:
    normalized = color.strip().lstrip("#").lower()
    if len(normalized) != 6 or any(char not in "0123456789abcdef" for char in normalized):
        raise ValueError(f"Invalid label color: {color}")
    return normalized


def load_desired_labels(path: Path) -> list[Label]:
    raw_labels = json.loads(path.read_text(encoding="utf-8"))
    labels: list[Label] = []
    seen: set[str] = set()

    for item in raw_labels:
        label = Label(
            name=str(item["name"]).strip(),
            color=normalize_color(str(item["color"])),
            description=str(item.get("description", "")).strip(),
        )
        if not label.name:
            raise ValueError("Label name must not be empty")
        key = label.name.casefold()
        if key in seen:
            raise ValueError(f"Duplicate label in config: {label.name}")
        seen.add(key)
        labels.append(label)

    return labels


def fetch_existing_labels(repo: str) -> dict[str, Label]:
    result = run_gh(
        [
            "label",
            "list",
            "--repo",
            repo,
            "--limit",
            "1000",
            "--json",
            "name,color,description",
        ]
    )
    require_success(result, "Fetching labels")
    labels = {}

    for item in json.loads(result.stdout):
        label = Label(
            name=str(item["name"]),
            color=normalize_color(str(item["color"])),
            description=str(item.get("description") or ""),
        )
        labels[label.name.casefold()] = label

    return labels


def label_diff(desired: Label, existing: Label | None) -> list[str]:
    if existing is None:
        return ["missing"]

    changes = []
    if desired.color != existing.color:
        changes.append(f"color {existing.color} -> {desired.color}")
    if desired.description != existing.description:
        changes.append("description")
    return changes


def sync_label(repo: str, label: Label, existing: Label | None) -> None:
    if existing is None:
        result = run_gh(
            [
                "label",
                "create",
                label.name,
                "--repo",
                repo,
                "--color",
                label.color,
                "--description",
                label.description,
            ]
        )
        require_success(result, f"Creating label {label.name}")
        return

    result = run_gh(
        [
            "label",
            "edit",
            existing.name,
            "--repo",
            repo,
            "--color",
            label.color,
            "--description",
            label.description,
        ]
    )
    require_success(result, f"Updating label {label.name}")


def main() -> int:
    args = parse_args()
    labels_path = Path(args.labels)

    try:
        repo = resolve_repo(args.repo)
        desired_labels = load_desired_labels(labels_path)
        existing_labels = fetch_existing_labels(repo)
    except (OSError, KeyError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"Label sync failed: {exc}", file=sys.stderr)
        return 1

    pending: list[tuple[Label, Label | None, list[str]]] = []
    for label in desired_labels:
        existing = existing_labels.get(label.name.casefold())
        changes = label_diff(label, existing)
        if changes:
            pending.append((label, existing, changes))

    if not pending:
        print(f"Labels are already in sync for {repo}.")
        return 0

    for label, existing, changes in pending:
        action = "create" if existing is None else "update"
        print(f"{action}: {label.name} ({', '.join(changes)})")

    if args.check:
        print(f"{len(pending)} label change(s) required.")
        return 1

    try:
        for label, existing, _changes in pending:
            sync_label(repo, label, existing)
    except RuntimeError as exc:
        print(f"Label sync failed: {exc}", file=sys.stderr)
        return 1

    print(f"Synced {len(pending)} label(s) for {repo}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
