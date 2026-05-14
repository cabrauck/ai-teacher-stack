# DOCX Document Factory Plan

Status: Planning

## Goal

Create a future implementation path for generating classroom-ready DOCX documents from Markdown and lesson data while keeping Markdown useful as the durable source, with ODT as an open-format output path for LibreOffice-compatible workflows.

## Plan Shape

- Save this hybrid spec skeleton for Agent OS and backlog tracking.
- Confirm output types and file naming before implementation.
- Keep document export isolated in `teacher_tools/documents.py`.
- Keep ODT output aligned with the same source Markdown, filenames, and review-note requirements as DOCX.
- Add focused tests once behavior is implemented.

## Current Decision

This spec is v1 planning only. No DOCX or ODT rendering, template, API, or export behavior changes are implemented by this skeleton.
