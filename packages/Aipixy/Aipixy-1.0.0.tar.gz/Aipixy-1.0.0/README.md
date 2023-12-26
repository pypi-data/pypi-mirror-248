# Aipixy Python Library

A Python library for the Aipixy API, enabling the generation of personalized and dynamic clone videos.

## Documentation
For comprehensive information on the Aipixy API, refer to the [Aipixy API Documentation](https://developers.aipixy.com/).

## Requirements
- Python 3.4 or higher versions

## Installation
Install the Aipixy library using the following pip command:

```bash
pip install Aipixy
```

## Authentication
To use the Aipixy library, you need to obtain your API key from the Aipixy platform. Retrieve your API key from the settings page on the Aipixy platform.

### Create an Aipixy instance
Once you have obtained your API key, create an Aipixy instance in your Python code:

```python
from Aipixy import Aipixy

# Replace 'YOUR_API_KEY' with your actual API key
ap = Aipixy(api_key='YOUR_API_KEY')
```

# Account Information
Retrieve information about your Aipixy account status using the following code snippet:
```python
# Get account information
account_information = ap.account()
```

Feel free to explore the Aipixy library and integrate it into your projects for dynamic clone video generation. If you encounter any issues or have questions, refer to the [Aipixy API Documentation](https://developers.aipixy.com/) or reach out to Aipixy support.


