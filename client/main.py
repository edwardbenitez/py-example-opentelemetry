"""Client application for consuming fruits API with OpenTelemetry instrumentation."""

import logging
import os
import time
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
    
    # Get API URL from environment variable or use default
    api_url = os.getenv("API_URL", "http://localhost:8000")
    logger.info(f"Configured API URL: {api_url}")
    
    # Run continuously, fetching fruits at regular intervals
    fetch_interval = 30  # seconds between fetches
    
    try:
        iteration = 0
        while True:
            iteration += 1
            logger.info(f"Fruits Client iteration {iteration} starting")
            try:
                fetch_and_print_fruits(api_url)
                logger.info(f"Iteration {iteration} completed successfully")
            except Exception as e:
                logger.error(f"Iteration {iteration} failed: {str(e)}", exc_info=True)
                # Continue looping even if one iteration fails
            
            logger.debug(f"Sleeping for {fetch_interval} seconds before next fetch")
            time.sleep(fetch_interval)
    except KeyboardInterrupt:
        logger.info("Fruits Client interrupted by user")
    except Exception as e:
        logger.error(f"Client encountered fatal error: {str(e)}", exc_info=True)
        exit(1)


if __name__ == "__main__":
    main()
