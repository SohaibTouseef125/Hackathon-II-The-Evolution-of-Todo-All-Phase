import sys
import os
# Add the backend directory to the Python path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp.server.stdio import stdio_server
from mcp_server.tools import app
import asyncio


async def main():
    """
    Main entry point for the MCP server.
    This runs the server using stdio protocol.
    """
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())