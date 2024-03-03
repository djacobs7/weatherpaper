import requests
from datetime import datetime

def display_today_detailed_forecast(api_endpoint, latitude, longitude):
    # Construct the API URL
    url = f"{api_endpoint}/points/{latitude},{longitude}"

    # Make the API request
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the forecast URL
        forecast_url = data['properties']['forecast']

        # Make a request to the forecast URL
        forecast_response = requests.get(forecast_url)

        if forecast_response.status_code == 200:
            # Parse the forecast JSON response
            forecast_data = forecast_response.json()

            # Extract today's date
            today_date = datetime.now().strftime('%Y-%m-%d')

            # Display detailed forecast for today
            print("Today's Detailed Forecast:")
            for period in forecast_data['properties']['periods']:
                if period['startTime'].startswith(today_date):
                    print(f"  {period['name']}: {period['detailedForecast']}")
        else:
            print(f"Failed to fetch forecast data. Status code: {forecast_response.status_code}")
    else:
        print(f"Failed to fetch weather data. Status code: {response.status_code}")

# Latitude and longitude for a location (e.g., Baltimore)
latitude = 39.2904
longitude = -76.6122

# API endpoint for weather.gov
api_endpoint = "https://api.weather.gov"

# Example usage
display_today_detailed_forecast(api_endpoint, latitude, longitude)