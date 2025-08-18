{% if file_headers %}# {{ file_headers_copyright }}{% endif %}
"""CLI entry-point launching the {{ mcp_name | capitalize }} WebSocket upstream (for external a2a-proxy)."""
import click
from .server import main as _run

@click.command()
@click.option("--host", default="0.0.0.0", help="Bind address")
@click.option("--port", default=8000, help="Port to serve on")
def cli(host: str, port: int) -> None:
    """Start the WebSocket proxy."""
    _run(host, port)

if __name__ == "__main__":
    cli()
