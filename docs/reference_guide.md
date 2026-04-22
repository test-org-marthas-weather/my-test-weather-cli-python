# Library Reference Guide 📚

This document provides a comprehensive reference for the Python libraries used in this Weather CLI project, compiled from official documentation via Context7.

---

## Table of Contents

1. [Requests Library](#requests-library)
2. [Click Library](#click-library)
3. [Best Practices](#best-practices)

---

## Requests Library

**Official Documentation:** https://requests.readthedocs.io/

**Purpose:** Requests is a simple, elegant, and widely-used Python HTTP library that makes sending HTTP requests incredibly easy, supporting features like connection pooling, authentication, and automatic content decompression.

### Basic GET Request

The fundamental pattern for making HTTP requests to REST APIs:

```python
import requests

# Simple GET request
r = requests.get('https://api.github.com/user', auth=('user', 'pass'))

# Check status code
print(r.status_code)  # 200

# Access headers
print(r.headers['content-type'])  # 'application/json; charset=utf8'

# Get response encoding
print(r.encoding)  # 'utf-8'

# Access raw text
print(r.text)  # '{"type":"User"...'

# Parse JSON response
data = r.json()
print(data)  # {'private_gists': 419, 'total_private_repos': 77, ...}
```

### Handling JSON Responses

The `.json()` method provides convenient JSON decoding:

```python
import requests
import json

# Make API request
r = requests.get('https://api.github.com/repos/psf/requests/git/commits/a050faf084662f3a352dd1a941f2c7c9f886d4ad')

# Check if request was successful
if r.status_code == requests.codes.ok:
    # Print content type
    print(r.headers['content-type'])
    
    # Parse JSON response
    commit_data = r.json()
    
    # Access specific data
    print(commit_data.keys())
    print(commit_data['committer'])
    print(commit_data['message'])
else:
    print(f"Request failed with status code: {r.status_code}")
```

### Error Handling

Requests provides a comprehensive exception hierarchy for robust error handling:

```python
import requests

try:
    response = requests.get('https://httpbin.org/delay/5', timeout=3)
    response.raise_for_status()  # Raise exception for bad status codes
    data = response.json()
    
except requests.exceptions.Timeout as e:
    print(f"The request timed out: {e}")
    
except requests.exceptions.ConnectionError as e:
    print(f"A connection error occurred: {e}")
    
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
    
except requests.exceptions.JSONDecodeError as e:
    print(f"Failed to decode JSON: {e}")
    
except requests.exceptions.RequestException as e:
    print(f"An unexpected error occurred: {e}")
```

### Exception Hierarchy

- **`RequestException`** - Base exception for all Requests errors
  - **`ConnectionError`** - Connection issues (DNS failure, refused connection)
    - `ConnectTimeout`
    - `ProxyError`
    - `SSLError`
  - **`HTTPError`** - Bad HTTP status codes (4xx or 5xx)
  - **`Timeout`** - Request timeout
    - `ConnectTimeout` - Connection timeout
    - `ReadTimeout` - Server didn't send data in time
  - **`TooManyRedirects`** - Exceeded maximum redirects
  - **`JSONDecodeError`** - Invalid JSON in response

### Important Notes

⚠️ **Success Check:** A successful `r.json()` call doesn't guarantee HTTP success. Always check `r.status_code` or use `r.raise_for_status()`.

⚠️ **JSON Errors:** `r.json()` raises `JSONDecodeError` for:
- 204 No Content responses
- Invalid JSON data
- Empty responses

---

## Click Library

**Official Documentation:** https://click.palletsprojects.com/

**Purpose:** Click is a Python composable command-line interface toolkit that makes creating beautiful command-line interfaces quick and fun while preventing common mistakes.

### Basic CLI Command

Create a simple command with options:

```python
import click

@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == '__main__':
    hello()
```

### Adding Parameters

Click supports two types of parameters:

#### 1. Options (with `--` prefix)

```python
@click.command()
@click.option('--count', default=1, help='number of greetings')
def hello(count):
    for x in range(count):
        click.echo(f"Hello!")
```

#### 2. Arguments (positional)

```python
@click.command()
@click.option('--count', default=1, help='number of greetings')
@click.argument('name')
def hello(count, name):
    for x in range(count):
        click.echo(f"Hello {name}!")
```

### Option Naming Conventions

Click automatically converts option names to Python identifiers:

**Explicit naming:**
```python
@click.command()
@click.option('--string-to-echo', 'string_to_echo')
def echo(string_to_echo):
    click.echo(string_to_echo)
```

**Automatic inference:**
```python
@click.command()
@click.option('--string-to-echo')  # Becomes 'string_to_echo' parameter
def echo(string_to_echo):
    click.echo(string_to_echo)
```

### Common Option Features

- **Default values:** `default=1`
- **Help text:** `help='Description of option'`
- **Prompts:** `prompt="Your name"` - Interactively ask for input
- **Type conversion:** Click automatically converts types
- **Required options:** `required=True`
- **Multiple values:** `multiple=True`

### Best Practices for CLI Design

1. **Use `click.echo()` instead of `print()`** - Better for testing and output handling
2. **Provide helpful descriptions** - Use docstrings and help text
3. **Set sensible defaults** - Make the CLI user-friendly
4. **Use arguments for required inputs** - Use options for optional flags
5. **Group related commands** - Use `@click.group()` for complex CLIs

---

## Best Practices

### For Weather CLI Application

#### 1. API Request Pattern

```python
import requests
import click
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@click.command()
@click.option('--city', prompt='City name', help='City to get weather for')
@click.option('--units', default='metric', help='Units: metric, imperial, or kelvin')
def get_weather(city, units):
    """Fetch current weather for a city."""
    api_key = os.getenv('WEATHER_API_KEY')
    
    if not api_key:
        click.echo("Error: WEATHER_API_KEY not found in environment", err=True)
        return
    
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': units
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Display weather information
        click.echo(f"\n🌤️  Weather in {data['name']}, {data['sys']['country']}")
        click.echo(f"Temperature: {data['main']['temp']}°")
        click.echo(f"Conditions: {data['weather'][0]['description']}")
        click.echo(f"Humidity: {data['main']['humidity']}%")
        
    except requests.exceptions.Timeout:
        click.echo("Error: Request timed out", err=True)
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            click.echo(f"Error: City '{city}' not found", err=True)
        else:
            click.echo(f"Error: HTTP {response.status_code}", err=True)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)
    except KeyError:
        click.echo("Error: Unexpected response format", err=True)

if __name__ == '__main__':
    get_weather()
```

#### 2. Environment Variable Management

Create a `.env` file:
```
WEATHER_API_KEY=your_api_key_here
```

Load in your application:
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('WEATHER_API_KEY')
```

#### 3. Error Handling Checklist

- ✅ Check for missing API keys
- ✅ Handle network timeouts
- ✅ Handle HTTP errors (404, 401, 500, etc.)
- ✅ Handle JSON decode errors
- ✅ Validate response structure
- ✅ Provide user-friendly error messages

#### 4. Testing Your CLI

```bash
# Test with different cities
python main.py --city "London"
python main.py --city "Tokyo"

# Test with different units
python main.py --city "Paris" --units imperial

# Test error handling
python main.py --city "InvalidCityName123"

# Get help
python main.py --help
```

---

## Additional Resources

- **Requests Documentation:** https://requests.readthedocs.io/
- **Click Documentation:** https://click.palletsprojects.com/
- **OpenWeatherMap API:** https://openweathermap.org/api
- **Python dotenv:** https://pypi.org/project/python-dotenv/

---

*This reference guide was compiled using Context7 documentation tools to provide accurate, up-to-date information from official sources.*
