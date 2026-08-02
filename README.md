# Weather Assistant Bot

A Python-based weather assistant that provides real-time weather information for any city using a weather API.

## Features

- Search weather by city
- Display current temperature
- Display humidity
- Display wind speed
- Display weather conditions
- Handle invalid city names gracefully

## Technologies Used

- Python 3
- Requests
- Weather API (e.g., OpenWeatherMap)

## Project Structure

```
Weather-Assistant-Bot/
│── main.py
│── weather.py
│── long_responses.py
│── requirements.txt
└── README.md
```

## Installation

### Clone the repository

```bash
git clone https://github.com/cyberookie-cookie/Weather-Assistant-Bot.git
cd Weather-Assistant-Bot
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure the API key

Open `weather.py` and replace the placeholder with your API key.

```python
API_KEY = "YOUR_API_KEY"
```

### Run the application

```bash
python main.py
```

## Example

```
You: weather in Florida
Clima: 📍 Florida, US
🌡️ Temperature: 26.63°C (feels like 26.63°C)
☁️ Condition: Overcast clouds
💧 Humidity: 93%
💨 Wind: 0.45 m/s
```

## Future Improvements

- 5-day weather forecast
- Air quality information
- Weather alerts
- Graphical user interface
- Voice assistant support

## Author

**cyberookie-cookie**
