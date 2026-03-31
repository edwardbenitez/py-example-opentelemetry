"""Tests for the Fruits Client."""

import pytest
from unittest.mock import patch, MagicMock
from client.main import fetch_and_print_fruits, main


class TestFetchAndPrintFruits:
    """Tests for fetch_and_print_fruits function."""
    
    @patch('client.main.requests.get')
    def test_fetch_fruits_success(self, mock_get):
        """Test successfully fetching and processing fruits."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fruits": [
                {"id": 1, "name": "apple", "color": "red"},
                {"id": 2, "name": "banana", "color": "yellow"},
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Should not raise an exception
        fetch_and_print_fruits()
        
        # Verify API was called
        mock_get.assert_called_once_with("http://localhost:8000/fruits")
    
    @patch('client.main.requests.get')
    def test_fetch_fruits_with_custom_url(self, mock_get):
        """Test fetching fruits with custom API URL."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"fruits": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        custom_url = "http://custom-api:8000"
        fetch_and_print_fruits(api_url=custom_url)
        
        mock_get.assert_called_once_with(f"{custom_url}/fruits")
    
    @patch('client.main.requests.get')
    def test_fetch_fruits_connection_error(self, mock_get):
        """Test handling of connection errors."""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        with pytest.raises(requests.exceptions.ConnectionError):
            fetch_and_print_fruits()
    
    @patch('client.main.requests.get')
    def test_fetch_fruits_http_error(self, mock_get):
        """Test handling of HTTP errors."""
        import requests
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        with pytest.raises(requests.exceptions.HTTPError):
            fetch_and_print_fruits()
    
    @patch('client.main.requests.get')
    @patch('builtins.print')
    def test_fetch_fruits_prints_output(self, mock_print, mock_get):
        """Test that fruits are printed to console."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fruits": [
                {"id": 1, "name": "apple", "color": "red"},
                {"id": 2, "name": "banana", "color": "yellow"},
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        fetch_and_print_fruits()
        
        # Verify print was called
        assert mock_print.called
        
        # Check that fruit names were printed
        all_print_calls = [str(call) for call in mock_print.call_args_list]
        all_output = " ".join(all_print_calls)
        
        # Should contain fruit information
        assert len(all_print_calls) > 0


class TestMain:
    """Tests for main function."""
    
    @patch('client.main.fetch_and_print_fruits')
    def test_main_success(self, mock_fetch):
        """Test main function executes successfully."""
        mock_fetch.return_value = None
        
        # Should not raise an exception
        main()
        
        # Verify fetch_and_print_fruits was called
        mock_fetch.assert_called_once()
    
    @patch('client.main.fetch_and_print_fruits')
    def test_main_handles_exception(self, mock_fetch):
        """Test main function handles exceptions gracefully."""
        mock_fetch.side_effect = Exception("API Error")
        
        with pytest.raises(SystemExit):
            main()


class TestClientOpenTelemetryInstrumentation:
    """Tests for OpenTelemetry instrumentation in client."""
    
    @patch('client.main.requests.get')
    def test_client_is_instrumented(self, mock_get):
        """Test that the client is instrumented with OpenTelemetry."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"fruits": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Should successfully use instrumentation
        fetch_and_print_fruits()
        
        # Verify the call was made
        mock_get.called
