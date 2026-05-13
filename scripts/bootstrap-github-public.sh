#!/usr/bin/env bash
set -euo pipefail

OWNER="${1:-cabrauck}"
REPO="${2:-ai-teacher-stack}"

if ! command -v git >/dev/null 2>&1; then
  echo "git is required." >&2
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI 'gh' is required." >&2
  echo "Install and authenticate with: gh auth login" >&2
  exit 1
fi

if [ -d .git ]; then
  echo "Git repository already initialized."
else
  git init
fi

git add .
if git diff --cached --quiet; then
  echo "No changes to commit."
else
  git commit -m "Initial ai-teacher-stack scaffold"
fi

if gh repo view "${OWNER}/${REPO}" >/dev/null 2>&1; then
  echo "Repository ${OWNER}/${REPO} already exists."
  git remote remove origin >/dev/null 2>&1 || true
  git remote add origin "https://github.com/${OWNER}/${REPO}.git"
  git push -u origin HEAD
else
  gh repo create "${OWNER}/${REPO}" --public --source=. --remote=origin --push
fi

echo "Done: https://github.com/${OWNER}/${REPO}"
