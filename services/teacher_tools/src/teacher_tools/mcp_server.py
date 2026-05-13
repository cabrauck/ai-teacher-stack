"""MCP wrapper placeholder.

The initial runtime uses FastAPI because it is easy to test locally and through
Docker. A later milestone should wrap the same pure functions with an MCP
server for Claude Code, Codex, or other MCP clients.

Keep all real logic in teacher_tools.curriculum, teacher_tools.lessons, and
teacher_tools.documents so the API and MCP surfaces stay consistent.
"""
