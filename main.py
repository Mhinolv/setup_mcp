from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context
import asyncio
import subprocess
from typing import Optional
import os

# Create the MCP server
mcp = FastMCP("Setup MCP Server")

SETUP_MD_PATH = os.path.join(os.path.dirname(__file__), "SETUP.md")

@mcp.resource("setup://instructions")
def get_setup_instructions() -> str:
    """
    Get the contents of the SETUP.md file as setup instructions.
    Returns:
        The contents of SETUP.md as a string.
    """
    if not os.path.exists(SETUP_MD_PATH):
        return "SETUP.md file not found."
    try:
        with open(SETUP_MD_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading SETUP.md: {str(e)}"

@mcp.tool()
async def terminal_tool(command: str, timeout: Optional[int] = 30, ctx: Optional[Context] = None) -> dict:
    """
    Execute a shell command on the server and return its output.
    Args:
        command: The shell command to execute.
        timeout: Maximum time in seconds to allow the command to run (default: 30).
    Returns:
        A dictionary with 'stdout', 'stderr', and 'exit_code'.
    """
    if not command.strip():
        return {"isError": True, "content": [{"type": "text", "text": "No command provided."}]}
    try:
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            proc.kill()
            return {"isError": True, "content": [{"type": "text", "text": f"Command timed out after {timeout} seconds."}]}
        return {
            "stdout": stdout.decode("utf-8", errors="replace"),
            "stderr": stderr.decode("utf-8", errors="replace"),
            "exit_code": proc.returncode,
        }
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": f"Error executing command: {str(e)}"}]}

if __name__ == "__main__":
    mcp.run()
