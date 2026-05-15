from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path


def test_release_package_contains_schriftwesen_runtime_templates_and_skeletons(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[3]
    output_dir = tmp_path / "dist"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_release.py",
            "--version",
            "test",
            "--output-dir",
            str(output_dir),
            "--check",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    archive_path = output_dir / "ai-teacher-stack-user-test.zip"
    with zipfile.ZipFile(archive_path) as archive:
        members = set(archive.namelist())

    assert "ai-teacher-stack/templates/schriftwesen/wochenplan.template.md" in members
    assert (
        "ai-teacher-stack/templates/schriftwesen/top-tagesorganisationsplan.template.md"
        in members
    )
    assert "ai-teacher-stack/vault/Schriftwesen/.gitkeep" in members
    assert "ai-teacher-stack/vault/Sources/.gitkeep" in members
    assert "ai-teacher-stack/vault/Wiki/.gitkeep" in members
    assert "ai-teacher-stack/vault/Templates/Schriftwesen/.gitkeep" in members
    assert "ai-teacher-stack/.claude-os/data/.gitkeep" in members
    assert "ai-teacher-stack/.librechat/.gitkeep" in members
    assert "ai-teacher-stack/.librechat/mongodb/.gitkeep" in members
    assert "ai-teacher-stack/.librechat/uploads/.gitkeep" in members
    assert "ai-teacher-stack/integrations/claude-os/bootstrap_vault.py" in members
    assert "ai-teacher-stack/integrations/claude-os/Dockerfile" in members
    assert "ai-teacher-stack/integrations/claude-os/entrypoint.sh" in members
    assert "ai-teacher-stack/integrations/librechat/librechat.yaml" in members
    assert "ai-teacher-stack/scripts/start-pre-release.ps1" in members
    assert "ai-teacher-stack/scripts/start-pre-release.sh" in members
    assert "ai-teacher-stack/scripts/check-pre-release.ps1" in members
    assert "ai-teacher-stack/scripts/check-pre-release.sh" in members
    assert "ai-teacher-stack/scripts/stop-pre-release.ps1" in members
    assert "ai-teacher-stack/scripts/stop-pre-release.sh" in members
    assert "ai-teacher-stack/docs/pre-release-guide.md" in members
    assert "ai-teacher-stack/services/teacher_tools/src/teacher_tools/stack_status.py" in members
    assert "ai-teacher-stack/services/teacher_tools/src/teacher_tools/mcp_server.py" in members
    assert (
        "ai-teacher-stack/agent-os/specs/2026-05-14-schriftwesen-und-uebergabe/spec.md"
        not in members
    )
    assert (
        "ai-teacher-stack/agent-os/specs/2026-05-14-enduser-pre-release/spec.md"
        not in members
    )
    assert "ai-teacher-stack/.claude/commands/agent-os/shape-spec.md" not in members
    assert "ai-teacher-stack/AGENTS.md" not in members
    assert "ai-teacher-stack/CLAUDE.md" not in members
    assert "ai-teacher-stack/.librechat/mongodb/librechat.db" not in members
    assert "ai-teacher-stack/.librechat/logs/app.log" not in members
    assert "ai-teacher-stack/docs/agent-client-setup.md" not in members
