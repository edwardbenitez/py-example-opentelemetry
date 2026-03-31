"""
OpenTelemetry Fruits API - Main Entry Point

This project implements an OpenTelemetry-instrumented API and client.

To run the API:
    uv run python -m api.main

To run the client:
    uv run python -m client.main

To run with Docker Compose (full observability stack):
    docker-compose up

To run tests:
    uv run pytest tests/ -v

For more information, see README.md
"""

from client.main import main


if __name__ == "__main__":
    main()
