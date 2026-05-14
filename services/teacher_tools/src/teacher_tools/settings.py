import os
from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    curriculum_root: Path = Path(os.getenv("CURRICULUM_ROOT", "/app/data/curriculum"))
    vault_root: Path = Path(os.getenv("VAULT_ROOT", "/app/vault"))
    export_root: Path = Path(os.getenv("EXPORT_ROOT", "/app/exports"))
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
    ollama_default_model: str = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3.1:8b")
    claude_os_url: str = os.getenv("CLAUDE_OS_URL", "http://claude-os:8051")
    claude_os_index_root: Path = Path(os.getenv("CLAUDE_OS_INDEX_ROOT", "/app/vault/Wiki"))
    memory_require_privacy_validation: bool = (
        os.getenv("MEMORY_REQUIRE_PRIVACY_VALIDATION", "true").lower() == "true"
    )
    enable_cloud_exports: bool = os.getenv("ENABLE_CLOUD_EXPORTS", "false").lower() == "true"
    enable_student_data: bool = os.getenv("ENABLE_STUDENT_DATA", "false").lower() == "true"


settings = Settings()
