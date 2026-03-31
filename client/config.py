"""OpenTelemetry configuration for the client."""

import logging
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
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


def setup_traces():
    """Setup OTLP trace exporter for Tempo."""
    otlp_exporter = OTLPSpanExporter(
        endpoint="http://tempo:4317",
        insecure=True,
    )
    trace_provider = TracerProvider()
    trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    trace.set_tracer_provider(trace_provider)
    return trace_provider


def setup_instrumentation():
    """Setup OpenTelemetry auto-instrumentation."""
    RequestsInstrumentor().instrument()


def initialize_telemetry():
    """Initialize all OpenTelemetry components."""
    logger = setup_logging()
    trace_provider = setup_traces()
    setup_instrumentation()
    
    logger.info("OpenTelemetry initialized successfully")
    return logger, trace_provider
