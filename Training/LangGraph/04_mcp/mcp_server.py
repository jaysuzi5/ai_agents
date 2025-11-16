from mcp.server.fastmcp import FastMCP  # Note: Import from mcp.server.fastmcp (standard)
from typing import Annotated
import operator

mcp = FastMCP("MathDemoServer")

@mcp.tool()
def add_numbers(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
    """Add two numbers."""
    return operator.add(a, b)

@mcp.tool()
def multiply_numbers(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
    """Multiply two numbers."""
    return operator.mul(a, b)

if __name__ == "__main__":
    # Run with streamable-http transport
    # Note: Host and port are typically configured via environment variables
    # or defaults to localhost:8000 for streamable-http
    mcp.run(transport="streamable-http")