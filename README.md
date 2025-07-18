# Setup MCP Server

A Model Context Protocol (MCP) server that provides setup instructions and terminal execution capabilities for Python development environments using uv.

## Overview

This MCP server serves as a helpful assistant for setting up Python development environments. It provides:

- **Setup Instructions Resource**: Access to comprehensive setup documentation via the `setup://instructions` resource
- **Terminal Tool**: Execute shell commands remotely with timeout protection
- **Development Environment Guidance**: Step-by-step instructions for uv, virtual environments, and dependency management

## Features

### Resources
- `setup://instructions` - Returns the contents of SETUP.md with detailed setup instructions

### Tools
- `terminal_tool` - Execute shell commands with configurable timeout (default: 30 seconds)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Mhinolv/setup_mcp.git
cd setup_mcp
```

2. Install dependencies using uv:
```bash
uv sync
```

## Usage

### Running the Server

```bash
uv run python main.py
```

### Using with MCP Clients

This server can be integrated with any MCP-compatible client. Configure your client to connect to this server to access:

- Setup instructions for Python development environments
- Remote terminal execution capabilities
- Development workflow guidance

### Example Resource Access

```python
# Access setup instructions
resource = client.get_resource("setup://instructions")
print(resource.content)  # Returns full SETUP.md content
```

### Example Tool Usage

```python
# Execute a shell command
result = await client.call_tool("terminal_tool", {
    "command": "uv --version",
    "timeout": 30
})
print(result["stdout"])  # Command output
```

## Configuration

### Environment Variables

The server supports standard MCP configuration through environment variables:

- `MCP_SERVER_NAME`: Override the default server name
- `MCP_LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)

### Timeout Settings

The terminal tool has a default timeout of 30 seconds, but this can be configured per command:

```python
result = await client.call_tool("terminal_tool", {
    "command": "long-running-command",
    "timeout": 120  # 2 minutes
})
```

## Security Considerations

- The terminal tool executes commands with the same privileges as the server process
- Commands are executed in the server's working directory
- Timeout protection prevents runaway processes
- All command output is captured and returned safely

## Development

### Project Structure

```
setup_mcp/
main.py           # MCP server implementation
SETUP.md          # Setup instructions resource
pyproject.toml    # Project configuration
uv.lock          # Dependency lock file
README.md        # This file
```

### Dependencies

- `fastmcp>=2.10.5` - FastMCP framework for building MCP servers
- `python-dotenv>=1.1.1` - Environment variable management

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests (if available)
5. Submit a pull request

## License

This project is open source. Please check the repository for license details.

## Support

For issues and questions:
- Open an issue on GitHub
- Check the SETUP.md file for environment setup help
- Review the MCP protocol documentation

## Related Documentation

- [SETUP.md](./SETUP.md) - Comprehensive setup instructions for Python development with uv
- [Model Context Protocol](https://modelcontextprotocol.io/) - Official MCP documentation
- [FastMCP](https://github.com/jlowin/fastmcp) - Framework used to build this server