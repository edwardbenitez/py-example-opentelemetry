"""FastAPI application for fruits listing service with OpenTelemetry instrumentation."""

import logging
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from opentelemetry import trace
from prometheus_client import REGISTRY, generate_latest

from api.config import initialize_telemetry

# Initialize OpenTelemetry
logger, prometheus_reader, meter_provider, trace_provider = initialize_telemetry()
tracer = trace.get_tracer(__name__)

app = FastAPI(title="Fruits API", version="1.0.0")

# Sample data: fruits and their colors
FRUITS = [
    {"id": 1, "name": "apple", "color": "red"},
    {"id": 2, "name": "banana", "color": "yellow"},
    {"id": 3, "name": "grape", "color": "purple"},
    {"id": 4, "name": "orange", "color": "orange"},
    {"id": 5, "name": "strawberry", "color": "red"},
    {"id": 6, "name": "blueberry", "color": "blue"},
    {"id": 7, "name": "kiwi", "color": "green"},
    {"id": 8, "name": "watermelon", "color": "green"},
]


@app.on_event("startup")
async def startup_event():
    """Log startup event."""
    logger.info("Fruits API starting up")


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown event."""
    logger.info("Fruits API shutting down")


@app.get("/")
async def root():
    """Root endpoint."""
    with tracer.start_as_current_span("root_endpoint"):
        logger.info("Root endpoint accessed")
        logger.debug("Returning welcome message")
        return {"message": "Welcome to Fruits API"}


@app.get("/fruits")
async def get_fruits():
    """Get all fruits with their colors.
    
    Returns:
        list: List of fruits with id, name, and color
    """
    with tracer.start_as_current_span("get_all_fruits"):
        logger.info("Fetching all fruits")
        logger.debug(f"Returning {len(FRUITS)} fruits")
        return {"fruits": FRUITS}


@app.get("/fruits/{fruit_id}")
async def get_fruit(fruit_id: int):
    """Get a specific fruit by ID.
    
    Args:
        fruit_id: The ID of the fruit
        
    Returns:
        dict: The fruit object or 404 if not found
    """
    with tracer.start_as_current_span("get_fruit_by_id") as span:
        span.set_attribute("fruit.id", fruit_id)
        logger.info(f"Fetching fruit with id: {fruit_id}")
        for fruit in FRUITS:
            if fruit["id"] == fruit_id:
                logger.debug(f"Found fruit: {fruit['name']}")
                return fruit
        logger.warning(f"Fruit with id {fruit_id} not found")
        return {"error": "Fruit not found"}, 404


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    with tracer.start_as_current_span("metrics_endpoint"):
        logger.info("Metrics endpoint accessed")
        logger.debug("Generating Prometheus metrics")
        return PlainTextResponse(
            generate_latest(REGISTRY).decode("utf-8"),
            media_type="text/plain; charset=utf-8"
        )


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Fruits API server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
