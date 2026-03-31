"""OpenTelemetry configuration for the API."""

import logging
from opentelemetry import metrics, trace
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


def setup_logging():
    """Setup console logging with OpenTelemetry context."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)


def setup_metrics():
    """Setup Prometheus metrics exporter."""
    prometheus_reader = PrometheusMetricReader()
    meter_provider = MeterProvider(metric_readers=[prometheus_reader])
    metrics.set_meter_provider(meter_provider)
    return prometheus_reader, meter_provider


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
    FastAPIInstrumentor().instrument()
    RequestsInstrumentor().instrument()


def initialize_telemetry():
    """Initialize all OpenTelemetry components."""
    logger = setup_logging()
    prometheus_reader, meter_provider = setup_metrics()
    trace_provider = setup_traces()
    setup_instrumentation()
    
    logger.info("OpenTelemetry initialized successfully")
    return logger, prometheus_reader, meter_provider, trace_provider
