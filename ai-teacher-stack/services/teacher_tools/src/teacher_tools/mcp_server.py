"""MCP wrapper placeholder.

The initial runtime uses FastAPI because it is easy to test locally and through
Docker. The next milestone should wrap the same pure functions with an MCP
server for Claude Code, Codex, or other MCP clients.

Suggested direction:

    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("ai-teacher-stack")

    @mcp.tool()
    def search_curriculum(query: str) -> dict:
        ...

    if __name__ == "__main__":
        mcp.run()

Keep all real logic in teacher_tools.curriculum, teacher_tools.lessons, and
teacher_tools.documents so the API and MCP surfaces stay consistent.
"""
