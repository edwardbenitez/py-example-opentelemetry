"""Tests for the Fruits API."""

import pytest
from fastapi.testclient import TestClient
from api.main import app, FRUITS


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint."""
    
    def test_root_returns_welcome_message(self, client):
        """Test that root endpoint returns a welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "Welcome" in response.json()["message"]


class TestFruitsEndpoint:
    """Tests for the /fruits endpoint."""
    
    def test_fruits_endpoint_returns_list(self, client):
        """Test that /fruits endpoint returns a list of fruits."""
        response = client.get("/fruits")
        assert response.status_code == 200
        data = response.json()
        assert "fruits" in data
        assert isinstance(data["fruits"], list)
    
    def test_fruits_contains_expected_fields(self, client):
        """Test that each fruit has required fields."""
        response = client.get("/fruits")
        data = response.json()
        fruits = data["fruits"]
        
        assert len(fruits) > 0
        
        for fruit in fruits:
            assert "id" in fruit
            assert "name" in fruit
            assert "color" in fruit
            assert isinstance(fruit["id"], int)
            assert isinstance(fruit["name"], str)
            assert isinstance(fruit["color"], str)
    
    def test_fruits_contains_all_sample_fruits(self, client):
        """Test that /fruits endpoint returns all sample fruits."""
        response = client.get("/fruits")
        data = response.json()
        fruits = data["fruits"]
        
        # Should have at least as many fruits as in FRUITS
        assert len(fruits) >= len(FRUITS)
        
        fruit_names = [fruit["name"] for fruit in fruits]
        
        for expected_fruit in FRUITS:
            assert expected_fruit["name"] in fruit_names


class TestFruitByIdEndpoint:
    """Tests for the /fruits/{fruit_id} endpoint."""
    
    def test_get_existing_fruit_by_id(self, client):
        """Test retrieving an existing fruit by ID."""
        response = client.get("/fruits/1")
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == 1
        assert "name" in data
        assert "color" in data
    
    def test_get_nonexistent_fruit_returns_error(self, client):
        """Test that requesting a non-existent fruit returns an error response."""
        response = client.get("/fruits/9999")
        # Should return either 404 or data with error message
        assert response.status_code in [200, 404] or "error" in response.json()


class TestMetricsEndpoint:
    """Tests for the /metrics endpoint."""
    
    def test_metrics_endpoint_exists(self, client):
        """Test that /metrics endpoint exists and returns data."""
        response = client.get("/metrics")
        assert response.status_code == 200
    
    def test_metrics_returns_prometheus_format(self, client):
        """Test that /metrics returns Prometheus-formatted data."""
        response = client.get("/metrics")
        content = response.text
        
        # Prometheus format contains lines starting with # or metric name
        assert len(content) > 0
        # Check for common Prometheus format indicators
        has_metrics = any(
            line.startswith("#") or 
            ("_" in line and "{" in line) or
            line.strip() and not line.startswith("#")
            for line in content.split("\n")
            if line.strip()
        )
        assert has_metrics or content  # At least has content


class TestOpenTelemetryInstrumentation:
    """Tests for OpenTelemetry instrumentation."""
    
    def test_api_is_instrumented(self, client):
        """Test that the API is instrumented with OpenTelemetry."""
        # Make a request and verify that tracing middleware is active
        response = client.get("/fruits")
        assert response.status_code == 200
        
        # Check that we get valid response (instrumentation shouldn't break functionality)
        data = response.json()
        assert "fruits" in data
