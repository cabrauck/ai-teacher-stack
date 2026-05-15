#!/usr/bin/env bash
set -euo pipefail

cd /opt/claude-os/frontend

python3 - <<'PY'
from __future__ import annotations

import os
from pathlib import Path

internal_api = os.getenv("CLAUDE_OS_API_INTERNAL_URL", "http://claude-os:8051")

vite_config = Path("vite.config.ts")
vite_text = vite_config.read_text(encoding="utf-8")
vite_text = vite_text.replace(
    "target: 'http://localhost:8051'",
    f"target: '{internal_api}'",
)
vite_text = vite_text.replace(
    """allowedHosts: [
      'localhost',
      '.ngrok-free.app',
      'daa65fe0204a.ngrok-free.app'
    ],""",
    "allowedHosts: true,",
)
vite_config.write_text(vite_text, encoding="utf-8")

for source in (Path("src/lib/api.ts"), Path("src/lib/auth.tsx")):
    source.write_text(
        source.read_text(encoding="utf-8").replace(
            "const API_BASE = 'http://localhost:8051';",
            "const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8051';",
        ),
        encoding="utf-8",
    )
PY

exec npm run dev -- --host 0.0.0.0 --port 5173
