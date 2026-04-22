# Weather CLI Tool 🌤️

A simple Python command-line interface (CLI) tool that fetches the current weather for a given city.

## Overview

This project demonstrates how to build a practical CLI application using Python's modern tooling. It combines the power of the `requests` library for HTTP API calls with the `click` library for creating an intuitive command-line interface.

## Features

- 🌍 Fetch current weather data for any city
- 🖥️ Clean and intuitive CLI interface
- 📊 Display temperature, conditions, and more
- 🔒 Secure API key management with environment variables

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/test-org-marthas-weather/my-test-weather-cli-python.git
cd my-test-weather-cli-python
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your weather API key:
   - Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/api) or similar service
   - Create a `.env` file in the project root:
   ```
   WEATHER_API_KEY=your_api_key_here
   ```

## Usage

Basic usage:
```bash
python main.py --city "London"
```

With additional options:
```bash
python main.py --city "New York" --units metric
```

Get help:
```bash
python main.py --help
```

## Libraries Used

This project leverages the following Python libraries:

- **[requests](https://requests.readthedocs.io/)** - Elegant HTTP library for making API calls
- **[click](https://click.palletsprojects.com/)** - Composable command-line interface toolkit
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** - Environment variable management

For detailed documentation on these libraries, see the [Reference Guide](docs/reference_guide.md).

## Project Structure

```
my-test-weather-cli-python/
├── .gitignore           # Python gitignore patterns
├── README.md            # This file
├── main.py              # Main CLI application
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
└── docs/
    └── reference_guide.md  # Library documentation reference
```

## Development

To contribute or modify this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

See the [Next Steps: Feature Roadmap](../../issues) issue for planned features and improvements.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Weather data provided by OpenWeatherMap API
- Built with Python, requests, and click
- Documentation powered by Context7

---

**Happy Weather Checking! ⛅**
