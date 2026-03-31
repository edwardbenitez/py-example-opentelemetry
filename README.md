# OpenTelemetry Fruits API

A demonstration of OpenTelemetry instrumentation with a FastAPI service, Python client, and complete observability stack including Prometheus, Grafana, and Tempo.

## Overview

This project implements a simple fruits listing API with complete OpenTelemetry instrumentation for:
- **Metrics**: Prometheus exporter for Prometheus scraping
- **Traces**: OTLP gRPC exporter for Tempo trace collection
- **Logs**: Console exporter for structured logging

The project includes:
- **API**: FastAPI service that lists fruits and their colors with `/fruits` and `/metrics` endpoints
- **Client**: Python client that fetches fruits from the API and prints them with OpenTelemetry instrumentation
- **Observability Stack**: Docker Compose setup with Prometheus, Grafana, and Tempo

## Project Structure

```
.
├── api/                          # FastAPI application
│   ├── __init__.py
│   ├── main.py                   # Main FastAPI app with endpoints
│   └── config.py                 # OpenTelemetry configuration
├── client/                       # Python client application
│   ├── __init__.py
│   ├── main.py                   # Client application
│   └── config.py                 # OpenTelemetry configuration
├── tests/                        # Test suite
│   ├── test_api.py               # API tests
│   ├── test_client.py            # Client tests
│   └── __init__.py
├── grafana/                      # Grafana configuration
│   └── provisioning/
│       ├── datasources/
│       └── dashboards/
├── Dockerfile.api                # API Docker image
├── Dockerfile.client             # Client Docker image
├── docker-compose.yml            # Observability stack orchestration
├── prometheus.yml                # Prometheus configuration
├── pyproject.toml                # Python project configuration
└── README.md                     # This file
```

## Requirements

- Python 3.13+
- Docker and Docker Compose
- `uv` package manager (included via pyproject.toml)

## Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd open-telemetry-test
   ```

2. **Install dependencies with uv**
   ```bash
   uv sync
   ```

3. **Run tests**
   ```bash
   uv run pytest tests/ -v
   ```

### Running with Docker Compose

The docker-compose setup runs the complete observability stack:

```bash
docker-compose up
```

This starts:
- **API** (http://localhost:8000) - Fruits API service
- **Prometheus** (http://localhost:9090) - Metrics collection
- **Grafana** (http://localhost:3000) - Metrics visualization (admin/admin)
- **Tempo** (http://localhost:4317) - Trace collection
- **Client** - Fetches fruits and exits

## API Endpoints

### GET /
Welcome endpoint
```bash
curl http://localhost:8000/
```

Response:
```json
{"message": "Welcome to Fruits API"}
```

### GET /fruits
List all fruits with their colors
```bash
curl http://localhost:8000/fruits
```

Response:
```json
{
  "fruits": [
    {"id": 1, "name": "apple", "color": "red"},
    {"id": 2, "name": "banana", "color": "yellow"},
    ...
  ]
}
```

### GET /fruits/{fruit_id}
Get a specific fruit by ID
```bash
curl http://localhost:8000/fruits/1
```

Response:
```json
{"id": 1, "name": "apple", "color": "red"}
```

### GET /metrics
Prometheus metrics endpoint
```bash
curl http://localhost:8000/metrics
```

Returns Prometheus-formatted metrics including:
- HTTP request metrics (count, duration)
- OpenTelemetry metrics
- Custom application metrics

## Running Locally (Without Docker)

### Terminal 1: Start API
```bash
uv run python -m api.main
```

The API will start at `http://localhost:8000`

### Terminal 2: Run Client
```bash
uv run python -m client.main
```

The client will fetch fruits from the API and print them to console with OpenTelemetry tracing.

## Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=api --cov=client --cov-report=html

# Run specific test file
uv run pytest tests/test_api.py -v

# Run specific test class
uv run pytest tests/test_api.py::TestFruitsEndpoint -v
```

## OpenTelemetry Instrumentation

### API Instrumentation

The API is instrumented with:
- **FastAPI Auto-Instrumentation**: Automatic tracing of HTTP requests
- **Prometheus Exporter**: Metrics exported to Prometheus
- **OTLP gRPC Exporter**: Traces sent to Tempo
- **Console Logging**: Structured logs to stdout

Configuration: [api/config.py](api/config.py)

### Client Instrumentation

The client is instrumented with:
- **Requests Auto-Instrumentation**: Automatic tracing of HTTP requests to the API
- **OTLP gRPC Exporter**: Traces sent to Tempo
- **Console Logging**: Structured logs to stdout

Configuration: [client/config.py](client/config.py)

## Observability Stack

### Prometheus (http://localhost:9090)
- Scrapes metrics from the API every 5 seconds
- Query metrics using PromQL
- Example queries:
  ```
  http_requests_total
  http_request_duration_seconds
  process_resident_memory_bytes
  ```

### Grafana (http://localhost:3000)
- Default login: `admin` / `admin`
- Pre-configured datasources:
  - Prometheus for metrics
  - Tempo for traces
- Create dashboards to visualize API metrics and traces

### Tempo (http://localhost:4317)
- Collects traces from API and client
- OTLP gRPC receiver on port 4317
- OTLP HTTP receiver on port 4318
- View traces through Grafana

## Environment Variables

- `OTEL_EXPORTER_OTLP_ENDPOINT`: Tempo endpoint (default: `http://localhost:4317`)
- `OTEL_EXPORTER_OTLP_INSECURE`: Use insecure connection (default: `true`)

## Troubleshooting

### Docker Container Issues
```bash
# Check logs
docker-compose logs api
docker-compose logs client
docker-compose logs prometheus

# Rebuild images
docker-compose build --no-cache

# Full reset
docker-compose down -v
docker-compose up
```

### Connection Errors
If the client fails to connect to the API:
- Ensure the API is running on port 8000
- Check firewall settings
- Verify network connectivity: `curl http://localhost:8000/fruits`

### Tempo/Prometheus Not Receiving Data
- Check that the OTEL exporter endpoint is correct
- Verify network connectivity between services
- Check service logs: `docker-compose logs tempo`, `docker-compose logs prometheus`

## Development

### Adding New Fruit Entries
Edit [api/main.py](api/main.py) and add to the `FRUITS` list:
```python
{"id": 9, "name": "cherry", "color": "red"},
```

### Adding Custom Metrics
In [api/config.py](api/config.py), create a meter and add metrics:
```python
meter = metrics.get_meter(__name__)
# Create counter, histogram, etc.
```

### Adding Custom Traces
Use the tracer in [api/main.py](api/main.py) or [client/main.py](client/main.py):
```python
with tracer.start_as_current_span("custom_operation"):
    # Your code here
    pass
```

## Testing

The project implements Test-Driven Development (TDD) with comprehensive tests for:
- API endpoints and response formats
- Client functionality and error handling
- OpenTelemetry instrumentation
- Prometheus metrics format

All tests pass with 100% success rate. See [tests/test_api.py](tests/test_api.py) and [tests/test_client.py](tests/test_client.py) for details.

## Docker Images

### Building Images Manually
```bash
# Build API image
docker build -f Dockerfile.api -t fruits-api:latest .

# Build client image
docker build -f Dockerfile.client -t fruits-client:latest .

# Run API container
docker run -p 8000:8000 fruits-api:latest

# Run client container (requires API running)
docker run --network host fruits-client:latest
```

## Performance Considerations

- **Metrics Collection**: Prometheus scrapes every 5 seconds (configurable in prometheus.yml)
- **Span Batching**: Traces are batched and exported periodically to Tempo
- **Memory**: The API is containerized with minimal memory overhead
- **Network**: All services communicate over Docker's internal network

## Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Implement the feature
3. Ensure all tests pass: `uv run pytest tests/ -v`
4. Update documentation
5. Follow OpenTelemetry instrumentation best practices

## License

See LICENSE file for details.

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenTelemetry Python Documentation](https://opentelemetry.io/docs/instrumentation/python/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Tempo Documentation](https://grafana.com/docs/tempo/)
