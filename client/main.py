"""Client application for consuming fruits API with OpenTelemetry instrumentation."""

import logging
import requests
from opentelemetry import trace

from client.config import initialize_telemetry

# Initialize OpenTelemetry
logger, trace_provider = initialize_telemetry()
tracer = trace.get_tracer(__name__)


def fetch_and_print_fruits(api_url: str = "http://localhost:8000"):
    """Fetch fruits from API and print them to console.
    
    Args:
        api_url: The base URL of the fruits API
    """
    with tracer.start_as_current_span("fetch_and_print_fruits") as span:
        span.set_attribute("api.url", api_url)
        logger.info(f"Starting to fetch fruits from {api_url}")
        logger.debug(f"API URL: {api_url}")
        
        try:
            with tracer.start_as_current_span("fetch_fruits_endpoint"):
                logger.info("Requesting /fruits endpoint")
                logger.debug(f"GET {api_url}/fruits")
                response = requests.get(f"{api_url}/fruits")
                response.raise_for_status()
                logger.debug(f"Response status: {response.status_code}")
            
            with tracer.start_as_current_span("process_fruits_response"):
                data = response.json()
                fruits = data.get("fruits", [])
                logger.info(f"Received {len(fruits)} fruits from API")
                logger.debug(f"Total fruits count: {len(fruits)}")
                
                print("\n" + "=" * 50)
                print("FRUITS AND THEIR COLORS")
                print("=" * 50)
                
                for fruit in fruits:
                    fruit_name = fruit.get("name", "Unknown")
                    fruit_color = fruit.get("color", "Unknown")
                    print(f"{fruit_name.capitalize()}: {fruit_color.capitalize()}")
                    logger.debug(f"Processed fruit: {fruit_name} (id={fruit.get('id')}, color={fruit_color})")
                
                print("=" * 50 + "\n")
                logger.info(f"Successfully displayed {len(fruits)} fruits")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch fruits: {str(e)}", exc_info=True)
            print(f"Error: Could not connect to API at {api_url}")
            raise


def main():
    """Main entry point for the client application."""
    logger.info("Fruits Client starting")
    try:
        fetch_and_print_fruits()
        logger.info("Client completed successfully")
    except Exception as e:
        logger.error(f"Client failed with error: {str(e)}", exc_info=True)
        exit(1)


if __name__ == "__main__":
    main()
