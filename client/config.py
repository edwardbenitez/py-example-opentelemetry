"""OpenTelemetry configuration for the client."""

import logging
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


def setup_logging():
    """Setup console logging with OpenTelemetry context."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)


def setup_traces(resource):
    """Setup OTLP trace exporter for Tempo."""
    otlp_exporter = OTLPSpanExporter(
        endpoint="http://tempo:4317",
        insecure=True,
    )
    trace_provider = TracerProvider(resource=resource)
    # Use BatchSpanProcessor with reasonable defaults:
    # - schedule_delay_millis: 5000ms (flush every 5 seconds)
    # - max_export_batch_size: 512 (max spans per batch)
    # - max_queue_size: 2048 (max spans in queue)
    trace_provider.add_span_processor(
        BatchSpanProcessor(
            otlp_exporter,
            schedule_delay_millis=5000,
            max_export_batch_size=512,
            max_queue_size=2048,
        )
    )
    trace.set_tracer_provider(trace_provider)
    return trace_provider


def setup_instrumentation():
    """Setup OpenTelemetry auto-instrumentation."""
    RequestsInstrumentor().instrument()


def initialize_telemetry():
    """Initialize all OpenTelemetry components."""
    logger = setup_logging()
    
    # Create resource to identify the service
    resource = Resource.create({
        "service.name": "fruits-client",
        "service.version": "1.0.0",
    })
    
    trace_provider = setup_traces(resource)
    setup_instrumentation()
    
    logger.info("OpenTelemetry initialized successfully")
    return logger, trace_provider
