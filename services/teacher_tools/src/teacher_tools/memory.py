from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from teacher_tools.privacy import (
    PrivacyValidationResult,
    assert_no_personal_data,
)

SOURCES_DIR = "Sources"
WIKI_DIR = "Wiki"
WIKI_INDEX = "index.md"
WIKI_LOG = "log.md"

TEACHER_MEMORY_NOTE = (
    "Hinweis: Diese Long-Term-Memory-Notiz ist ein lokal gespeicherter Entwurf. "
    "Vor Wiederverwendung fachlich, didaktisch und datenschutzrechtlich pruefen."
)

_TRANSLATION_TABLE = str.maketrans(
    {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss",
        "Ä": "ae",
        "Ö": "oe",
        "Ü": "ue",
    }
)


@dataclass(frozen=True)
class MemoryWriteResult:
    title: str
    slug: str
    path: Path
    relative_path: str
    privacy_status: str


@dataclass(frozen=True)
class MemoryPromotionResult:
    source_path: str
    wiki: MemoryWriteResult


def slugify(value: str, *, fallback: str = "untitled") -> str:
    normalized = value.strip().translate(_TRANSLATION_TABLE).casefold()
    slug = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    slug = slug[:80].strip("-")
    return slug or fallback


def ensure_memory_layout(vault_root: Path) -> None:
    (vault_root / SOURCES_DIR).mkdir(parents=True, exist_ok=True)
    (vault_root / WIKI_DIR).mkdir(parents=True, exist_ok=True)


def _now() -> datetime:
    return datetime.now(tz=UTC).replace(microsecond=0)


def _date_or_today(value: date | None) -> date:
    return value or _now().date()


def _relative_to_vault(vault_root: Path, path: Path) -> str:
    try:
        return path.relative_to(vault_root).as_posix()
    except ValueError:
        return path.as_posix()


def _resolve_inside_vault(vault_root: Path, path: str | Path) -> Path:
    root = vault_root.resolve()
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = root / candidate
    candidate = candidate.resolve()
    if not candidate.is_relative_to(root):
        raise ValueError(f"Memory path is outside the vault: {path}")
    return candidate


def _yaml_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, date | datetime):
        return value.isoformat()
    text = str(value).replace("\n", " ").strip()
    if not text:
        return '""'
    if any(char in text for char in [":", "#", "[", "]", "{", "}", '"']):
        return '"' + text.replace('"', '\\"') + '"'
    return text


def _frontmatter(metadata: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in metadata.items():
        if isinstance(value, list | tuple):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {_yaml_scalar(item)}")
        elif value is None:
            continue
        else:
            lines.append(f"{key}: {_yaml_scalar(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def _parse_frontmatter(markdown: str) -> dict[str, Any]:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break
    if end_index is None:
        return {}

    parsed: dict[str, Any] = {}
    for line in lines[1:end_index]:
        if not line.strip() or line.startswith(" ") or ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        value = raw_value.strip().strip('"')
        if value.casefold() == "true":
            parsed[key.strip()] = True
        elif value.casefold() == "false":
            parsed[key.strip()] = False
        else:
            parsed[key.strip()] = value
    return parsed


def _extract_markdown_field_markers(markdown: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    pattern = re.compile(r"^\s{0,3}([A-Za-zÄÖÜäöüß_][\wÄÖÜäöüß -]{1,60}):\s*(.*)$")
    for line in markdown.splitlines():
        match = pattern.match(line)
        if match:
            fields[match.group(1).strip()] = match.group(2).strip()
    return fields


def _strip_frontmatter(markdown: str) -> str:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        return markdown.strip()
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[index + 1 :]).strip()
    return markdown.strip()


def _title_from_markdown(markdown: str, fallback: str) -> str:
    frontmatter = _parse_frontmatter(markdown)
    title = str(frontmatter.get("title") or "").strip()
    if title:
        return title
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return fallback


def _read_wiki_title(path: Path) -> str:
    markdown = path.read_text(encoding="utf-8")
    return _title_from_markdown(markdown, path.stem)


def update_memory_index(vault_root: Path) -> Path:
    ensure_memory_layout(vault_root)
    wiki_root = vault_root / WIKI_DIR
    pages = sorted(
        path
        for path in wiki_root.glob("*.md")
        if path.name not in {WIKI_INDEX, WIKI_LOG}
    )

    lines = [
        "# Long-Term Memory Index",
        "",
        TEACHER_MEMORY_NOTE,
        "",
        "## Wiki-Seiten",
        "",
    ]
    if not pages:
        lines.append("_Noch keine Wiki-Seiten._")
    else:
        for page in pages:
            title = _read_wiki_title(page)
            lines.append(f"- [[{page.stem}|{title}]] (`{page.name}`)")

    index_path = wiki_root / WIKI_INDEX
    index_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return index_path


def append_memory_log(
    vault_root: Path,
    *,
    action: str,
    title: str,
    path: Path,
    timestamp: datetime | None = None,
) -> Path:
    ensure_memory_layout(vault_root)
    log_path = vault_root / WIKI_DIR / WIKI_LOG
    if not log_path.exists():
        log_path.write_text("# Long-Term Memory Log\n\n", encoding="utf-8")

    stamp = (timestamp or _now()).astimezone(UTC).replace(microsecond=0)
    relative = _relative_to_vault(vault_root, path)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"- {stamp.isoformat()} | {action} | `{relative}` | {title}\n")
    return log_path


def create_source_note(
    vault_root: Path,
    *,
    title: str,
    body: str,
    source_type: str = "note",
    tags: list[str] | None = None,
    created_at: date | None = None,
    metadata: dict[str, Any] | None = None,
) -> MemoryWriteResult:
    payload = {
        "title": title,
        "body": body,
        "body_fields": _extract_markdown_field_markers(body),
        "source_type": source_type,
        "tags": tags or [],
        "metadata": metadata or {},
    }
    validation = assert_no_personal_data(payload, context="memory source")

    ensure_memory_layout(vault_root)
    note_date = _date_or_today(created_at)
    slug = slugify(title)
    path = vault_root / SOURCES_DIR / f"{note_date.isoformat()}_{slug}.md"
    frontmatter = _frontmatter(
        {
            "type": "memory_source",
            "title": title,
            "slug": slug,
            "source_type": source_type,
            "created_at": note_date.isoformat(),
            "privacy_status": validation.privacy_status,
            "promoted": False,
            "tags": tags or [],
            **(metadata or {}),
        }
    )
    markdown = f"{frontmatter}# {title}\n\n{TEACHER_MEMORY_NOTE}\n\n{body.strip()}\n"
    path.write_text(markdown, encoding="utf-8")
    return MemoryWriteResult(
        title=title,
        slug=slug,
        path=path,
        relative_path=_relative_to_vault(vault_root, path),
        privacy_status=validation.privacy_status,
    )


def write_wiki_page(
    vault_root: Path,
    *,
    title: str,
    body: str,
    tags: list[str] | None = None,
    source_path: str | Path | None = None,
    updated_at: datetime | None = None,
    metadata: dict[str, Any] | None = None,
) -> MemoryWriteResult:
    payload = {
        "title": title,
        "body": body,
        "body_fields": _extract_markdown_field_markers(body),
        "tags": tags or [],
        "source_path": str(source_path) if source_path else None,
        "metadata": metadata or {},
    }
    validation = assert_no_personal_data(payload, context="memory wiki")

    ensure_memory_layout(vault_root)
    slug = slugify(title)
    path = vault_root / WIKI_DIR / f"{slug}.md"
    source_relative = None
    if source_path:
        resolved_source = _resolve_inside_vault(vault_root, source_path)
        source_relative = _relative_to_vault(vault_root, resolved_source)

    stamp = (updated_at or _now()).astimezone(UTC).replace(microsecond=0)
    frontmatter = _frontmatter(
        {
            "type": "memory_wiki",
            "title": title,
            "slug": slug,
            "updated_at": stamp.isoformat(),
            "privacy_status": validation.privacy_status,
            "source": source_relative,
            "tags": tags or [],
            **(metadata or {}),
        }
    )
    markdown = f"{frontmatter}# {title}\n\n{TEACHER_MEMORY_NOTE}\n\n{body.strip()}\n"
    path.write_text(markdown, encoding="utf-8")
    update_memory_index(vault_root)
    append_memory_log(vault_root, action="wiki_write", title=title, path=path, timestamp=stamp)
    return MemoryWriteResult(
        title=title,
        slug=slug,
        path=path,
        relative_path=_relative_to_vault(vault_root, path),
        privacy_status=validation.privacy_status,
    )


def promote_source_to_wiki(
    vault_root: Path,
    *,
    source_path: str | Path,
    title: str | None = None,
    summary: str | None = None,
    tags: list[str] | None = None,
    promoted_at: datetime | None = None,
) -> MemoryPromotionResult:
    ensure_memory_layout(vault_root)
    source = _resolve_inside_vault(vault_root, source_path)
    sources_root = (vault_root / SOURCES_DIR).resolve()
    if not source.is_relative_to(sources_root):
        raise ValueError(f"Only {SOURCES_DIR}/ notes can be promoted to the memory wiki.")
    if not source.is_file():
        raise FileNotFoundError(f"Memory source note does not exist: {source_path}")

    markdown = source.read_text(encoding="utf-8")
    frontmatter = _parse_frontmatter(markdown)
    field_markers = _extract_markdown_field_markers(markdown)
    validation_payload = {
        "frontmatter": frontmatter,
        "markdown_fields": field_markers,
        "title": title or _title_from_markdown(markdown, source.stem),
        "summary": summary or "",
        "tags": tags or [],
    }
    assert_no_personal_data(validation_payload, context="memory promotion")

    wiki_title = title or _title_from_markdown(markdown, source.stem)
    wiki_body = summary or _strip_frontmatter(markdown)
    wiki = write_wiki_page(
        vault_root,
        title=wiki_title,
        body=wiki_body,
        tags=tags,
        source_path=source,
        updated_at=promoted_at,
        metadata={"promoted_from": _relative_to_vault(vault_root, source)},
    )
    append_memory_log(vault_root, action="source_promoted", title=wiki_title, path=wiki.path)
    return MemoryPromotionResult(
        source_path=_relative_to_vault(vault_root, source),
        wiki=wiki,
    )


def read_memory_index(vault_root: Path) -> tuple[Path, str]:
    index_path = update_memory_index(vault_root)
    return index_path, index_path.read_text(encoding="utf-8")


def memory_health(vault_root: Path) -> dict[str, Any]:
    ensure_memory_layout(vault_root)
    sources = sorted((vault_root / SOURCES_DIR).glob("*.md"))
    wiki_pages = sorted(
        path
        for path in (vault_root / WIKI_DIR).glob("*.md")
        if path.name not in {WIKI_INDEX, WIKI_LOG}
    )
    return {
        "sources": len(sources),
        "wiki_pages": len(wiki_pages),
        "index_path": _relative_to_vault(vault_root, vault_root / WIKI_DIR / WIKI_INDEX),
        "log_path": _relative_to_vault(vault_root, vault_root / WIKI_DIR / WIKI_LOG),
    }


def validate_memory_payload(payload: Any) -> PrivacyValidationResult:
    return assert_no_personal_data(payload, context="memory payload")
