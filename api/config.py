"""OpenTelemetry configuration for the API."""

import logging
from opentelemetry import metrics, trace
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
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


def setup_metrics(resource):
    """Setup Prometheus metrics exporter."""
    prometheus_reader = PrometheusMetricReader()
    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[prometheus_reader]
    )
    metrics.set_meter_provider(meter_provider)
    return prometheus_reader, meter_provider


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
    FastAPIInstrumentor().instrument()
    RequestsInstrumentor().instrument()


def initialize_telemetry():
    """Initialize all OpenTelemetry components."""
    logger = setup_logging()
    
    # Create resource to identify the service
    resource = Resource.create({
        "service.name": "fruits-api",
        "service.version": "1.0.0",
    })
    
    prometheus_reader, meter_provider = setup_metrics(resource)
    trace_provider = setup_traces(resource)
    setup_instrumentation()
    
    logger.info("OpenTelemetry initialized successfully")
    return logger, prometheus_reader, meter_provider, trace_provider
