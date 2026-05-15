import os
from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    stack_public_host: str = os.getenv("STACK_PUBLIC_HOST", "localhost")
    host_librechat_port: int = int(os.getenv("HOST_LIBRECHAT_PORT", "3080"))
    host_teacher_tools_port: int = int(os.getenv("HOST_TEACHER_TOOLS_PORT", "8010"))
    host_claude_os_port: int = int(os.getenv("HOST_CLAUDE_OS_PORT", "8051"))
    host_claude_os_frontend_port: int = int(
        os.getenv("HOST_CLAUDE_OS_FRONTEND_PORT", "5173")
    )
    curriculum_root: Path = Path(os.getenv("CURRICULUM_ROOT", "/app/data/curriculum"))
    vault_root: Path = Path(os.getenv("VAULT_ROOT", "/app/vault"))
    export_root: Path = Path(os.getenv("EXPORT_ROOT", "/app/exports"))
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
    ollama_default_model: str = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3.1:8b")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    ollama_embed_model: str = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    claude_os_url: str = os.getenv("CLAUDE_OS_URL", "http://claude-os:8051")
    claude_os_frontend_url: str = os.getenv(
        "CLAUDE_OS_FRONTEND_URL",
        "http://claude-os-frontend:5173",
    )
    claude_os_redis_host: str = os.getenv("CLAUDE_OS_REDIS_HOST", "claude-os-redis")
    claude_os_redis_port: int = int(os.getenv("CLAUDE_OS_REDIS_PORT", "6379"))
    claude_os_index_root: Path = Path(os.getenv("CLAUDE_OS_INDEX_ROOT", "/app/vault/Wiki"))
    claude_os_project_name: str = os.getenv("CLAUDE_OS_PROJECT_NAME", "ai-teacher-stack")
    claude_os_wiki_kb_name: str = os.getenv(
        "CLAUDE_OS_WIKI_KB_NAME",
        "ai-teacher-stack-wiki",
    )
    claude_os_wiki_mcp_type: str = os.getenv("CLAUDE_OS_WIKI_MCP_TYPE", "project_memories")
    librechat_url: str = os.getenv("LIBRECHAT_URL", "http://librechat:3080")
    teacher_tools_mcp_host: str = os.getenv("TEACHER_TOOLS_MCP_HOST", "0.0.0.0")
    teacher_tools_mcp_port: int = int(os.getenv("TEACHER_TOOLS_MCP_PORT", "8020"))
    memory_require_privacy_validation: bool = (
        os.getenv("MEMORY_REQUIRE_PRIVACY_VALIDATION", "true").lower() == "true"
    )
    enable_cloud_exports: bool = os.getenv("ENABLE_CLOUD_EXPORTS", "false").lower() == "true"
    enable_student_data: bool = os.getenv("ENABLE_STUDENT_DATA", "false").lower() == "true"


settings = Settings()
