#!/usr/bin/env python3
"""
Weather CLI Tool
A simple command-line interface for fetching current weather data.
"""

import os
import sys
import click
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@click.command()
@click.option(
    '--city',
    prompt='City name',
    help='Name of the city to get weather for'
)
@click.option(
    '--units',
    default='metric',
    type=click.Choice(['metric', 'imperial', 'kelvin'], case_sensitive=False),
    help='Temperature units (metric=Celsius, imperial=Fahrenheit, kelvin=Kelvin)'
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Show detailed weather information'
)
def get_weather(city, units, verbose):
    """
    Fetch and display current weather for a given CITY.
    
    Examples:
    
        python main.py --city London
        
        python main.py --city "New York" --units imperial
        
        python main.py --city Tokyo --verbose
    """
    
    # Check for API key
    if not WEATHER_API_KEY:
        click.echo("❌ Error: WEATHER_API_KEY not found!", err=True)
        click.echo("Please set your API key in a .env file:", err=True)
        click.echo("  WEATHER_API_KEY=your_api_key_here", err=True)
        sys.exit(1)
    
    # Prepare API request
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': units
    }
    
    # Show loading message
    click.echo(f"🔍 Fetching weather data for {city}...")
    
    try:
        # Make API request
        response = requests.get(
            WEATHER_API_BASE_URL,
            params=params,
            timeout=10
        )
        
        # Raise exception for bad status codes
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Display weather information
        display_weather(data, units, verbose)
        
    except requests.exceptions.Timeout:
        click.echo("❌ Error: Request timed out. Please try again.", err=True)
        sys.exit(1)
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            click.echo(f"❌ Error: City '{city}' not found.", err=True)
            click.echo("Please check the spelling and try again.", err=True)
        elif response.status_code == 401:
            click.echo("❌ Error: Invalid API key.", err=True)
            click.echo("Please check your WEATHER_API_KEY in .env file.", err=True)
        else:
            click.echo(f"❌ Error: HTTP {response.status_code} - {e}", err=True)
        sys.exit(1)
        
    except requests.exceptions.ConnectionError:
        click.echo("❌ Error: Could not connect to weather service.", err=True)
        click.echo("Please check your internet connection.", err=True)
        sys.exit(1)
        
    except requests.exceptions.JSONDecodeError:
        click.echo("❌ Error: Invalid response from weather service.", err=True)
        sys.exit(1)
        
    except requests.exceptions.RequestException as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
        
    except KeyError as e:
        click.echo(f"❌ Error: Unexpected response format (missing key: {e})", err=True)
        sys.exit(1)


def display_weather(data, units, verbose):
    """
    Display formatted weather information.
    
    Args:
        data: Weather data dictionary from API
        units: Temperature units (metric, imperial, kelvin)
        verbose: Whether to show detailed information
    """
    # Determine temperature symbol
    temp_symbol = {
        'metric': '°C',
        'imperial': '°F',
        'kelvin': 'K'
    }.get(units, '°')
    
    # Extract weather data
    city_name = data['name']
    country = data['sys']['country']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    description = data['weather'][0]['description'].capitalize()
    wind_speed = data['wind']['speed']
    
    # Display basic information
    click.echo("\n" + "=" * 50)
    click.echo(f"🌤️  Weather in {city_name}, {country}")
    click.echo("=" * 50)
    click.echo(f"🌡️  Temperature: {temp}{temp_symbol}")
    click.echo(f"☁️  Conditions: {description}")
    click.echo(f"💧 Humidity: {humidity}%")
    
    # Display detailed information if verbose flag is set
    if verbose:
        click.echo(f"\n📊 Detailed Information:")
        click.echo(f"   Feels like: {feels_like}{temp_symbol}")
        click.echo(f"   Min temp: {temp_min}{temp_symbol}")
        click.echo(f"   Max temp: {temp_max}{temp_symbol}")
        click.echo(f"   Pressure: {pressure} hPa")
        click.echo(f"   Wind speed: {wind_speed} m/s")
        
        if 'clouds' in data:
            click.echo(f"   Cloudiness: {data['clouds']['all']}%")
        
        if 'visibility' in data:
            visibility_km = data['visibility'] / 1000
            click.echo(f"   Visibility: {visibility_km} km")
    
    click.echo("=" * 50 + "\n")


@click.command()
def version():
    """Display version information."""
    click.echo("Weather CLI Tool v1.0.0")
    click.echo("Built with Python, requests, and click")


# Create a command group for future expansion
@click.group()
def cli():
    """Weather CLI Tool - Fetch current weather for any city."""
    pass


# Add commands to the group
cli.add_command(get_weather, name='fetch')
cli.add_command(version)


if __name__ == '__main__':
    # For simple usage, call get_weather directly
    # For grouped commands, use: cli()
    get_weather()
