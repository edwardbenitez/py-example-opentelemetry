# Specification-Driven Development Instructions

## Overview

This application is looking to implement a simple API that lists fruits and their colors, along with a client that consumes this API. The application will be instrumented with OpenTelemetry for metrics, traces, and logs, and will be containerized using Docker.

## Process

### 1. Define Specifications
- This project must use UV as package manager.
- A fastapi dummy pipeline that list fruits and their colors
- A client that reads the fruits and their colors from the api and prints them to the console
- openapi is opentelemetry compliant and has a /metrics endpoint
- The api should be instrumented with opentelemetry and export metrics to a prometheus exporter
- The api should be instrumented with opentelemetry and export traces to a tempo exporter
- The api should be instrumented with opentelemetry and export logs to a console exporter
- Client should be instrumented with opentelemetry and export traces to a tempo exporter
- Client should be instrumented with opentelemetry and export logs to a console exporter
- Create the dockerfile for the api and client
- Create a docker-compose file to run the api, client, graphana, prometheus, tempo and console exporter
- use KISS approach for the implementation.
- Add tracing and logging to the api and client with appropriate spans and log messages to demonstrate the instrumentation.
- Ensure that the /metrics endpoint is properly exposed and can be scraped by Prometheus.
- Verify that the traces are being collected in Tempo and that logs are visible in the console.

### 2. Create Tests
- Write tests based on specifications
- Ensure tests validate all acceptance criteria
- Tests should fail before implementation

### 3. Implement Features
- Write code to satisfy specifications
- Ensure all tests pass
- Follow project coding standards

### 4. Code Review
- Verify implementation matches specification
- Confirm all tests pass
- Check for edge cases

### 5. Documentation
- Update relevant documentation
- Add examples if applicable
- Document any deviations from spec

## Guidelines
- Keep specifications concise and measurable
- One feature per specification when possible
- Review specifications before implementation begins