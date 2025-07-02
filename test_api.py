import requests

# My weather API key
api_key = "a8e89e424aca3ff1aea4807473839513"

# Cities I want to check
cities = ["London", "Paris", "Beirut", "Dubai", "Tokyo"]

print("Checking the weather...\n")

# Go through each city
for city in cities:
    try:
        # Ask the API for weather info
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        # Show temperature and weather
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        print(f"{city}: {temp}°C, {desc}")

    except:
        print(f"{city}: Something went wrong.")

print("\nDone!")
