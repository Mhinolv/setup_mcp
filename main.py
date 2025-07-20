import asyncio
import os
import re

from mcp.server.fastmcp import Context, FastMCP

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
        with open(SETUP_MD_PATH, encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                return "SETUP.md file is empty."
            return content
    except UnicodeDecodeError:
        return "Error: SETUP.md file contains invalid UTF-8 encoding."
    except PermissionError:
        return "Error: Permission denied reading SETUP.md file."
    except Exception as e:
        return f"Error reading SETUP.md: {str(e)}"


@mcp.tool()
async def terminal_tool(
    command: str, timeout: int | None = 30, ctx: Context | None = None
) -> dict:
    """
    Execute a shell command on the server and return its output.
    Args:
        command: The shell command to execute.
        timeout: Maximum time in seconds to allow the command to run (default: 30).
    Returns:
        A dictionary with 'stdout', 'stderr', and 'exit_code'.
    """
    # Input validation
    if not command or not command.strip():
        return {"stdout": "", "stderr": "No command provided.", "exit_code": 1}

    # Basic security checks - block dangerous commands
    dangerous_patterns = [
        r"rm\s+-rf\s+/",  # rm -rf /
        r":\(\)\{\s*:\|:\&\s*\}\s*;\s*:",  # fork bomb
        r">/dev/sd[a-z]",  # writing to disk devices
        r"dd\s+if=.*of=/dev/",  # dd to devices
        r"mkfs\.",  # filesystem creation
        r"fdisk\s+/dev/",  # disk partitioning
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            return {
                "stdout": "",
                "stderr": "Command blocked for security reasons.",
                "exit_code": 1,
            }

    # Validate timeout
    if timeout is not None and (timeout <= 0 or timeout > 300):
        return {
            "stdout": "",
            "stderr": "Timeout must be between 1 and 300 seconds.",
            "exit_code": 1,
        }

    try:
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except TimeoutError:
            proc.kill()
            return {
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds.",
                "exit_code": 124,
            }

        return {
            "stdout": stdout.decode("utf-8", errors="replace"),
            "stderr": stderr.decode("utf-8", errors="replace"),
            "exit_code": proc.returncode,
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Error executing command: {str(e)}",
            "exit_code": 1,
        }


if __name__ == "__main__":
    mcp.run()
