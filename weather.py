import requests
from datetime import datetime, timedelta
import random

class WeatherService:
    """This class gets weather info for a city"""

    def __init__(self):
        # Your weather API key
        self.api_key = "a8e89e424aca3ff1aea4807473839513"

    def get_forecast(self, city, days):
        """Get real weather. If it fails, use fake data"""
        try:
            city_name = city.split(',')[0]  # Get only the city part (e.g., "Beirut" from "Beirut, Lebanon")
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={self.api_key}&units=metric"
            
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                return self.parse_weather(data, days)
            else:
                print(f"API Error: {response.status_code}")
        except:
            print("⚠️ Failed to get real data")

        # If something goes wrong, return mock weather
        return self.generate_mock_weather(city, days)

    def parse_weather(self, data, days):
        """Pick one forecast per day"""
        forecast = []

        for i in range(0, days * 8, 8):  # Each 8 entries is about 1 day
            item = data['list'][i]
            forecast.append({
                'date': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d'),
                'temp': round(item['main']['temp']),
                'description': item['weather'][0]['description'],
                'icon': self.get_weather_icon(item['weather'][0]['main'])
            })

        return forecast

    def generate_mock_weather(self, city, days):
        """Fake weather if real one fails"""
        if 'Dubai' in city or 'Cairo' in city:
            base_temp = 35
        elif 'London' in city or 'Tokyo' in city:
            base_temp = 15
        else:
            base_temp = 22

        forecast = []
        for i in range(days):
            forecast.append({
                'date': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'),
                'temp': base_temp + random.randint(-5, 5),
                'description': random.choice(['sunny', 'cloudy', 'light rain']),
                'icon': random.choice(['☀️', '⛅', '🌧️'])
            })
        return forecast

    def get_weather_icon(self, weather_type):
        """Turn weather into emoji"""
        icons = {
            'Clear': '☀️',
            'Clouds': '☁️',
            'Rain': '🌧️',
            'Snow': '❄️'
        }
        return icons.get(weather_type, '⛅')  # Default: partly cloudy
