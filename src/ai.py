import requests
from datetime import datetime
from draw import draw_forecast

def get_forecast_data(api_endpoint, latitude, longitude):
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


            # Display detailed forecast for today

            return forecast_data
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


def render_forecast_data(forecast_data):
    # Extract today's date
    today_date = datetime.now().strftime('%Y-%m-%d')

    print("Today's Detailed Forecast:")
    for period in forecast_data['properties']['periods']:
        if period['startTime'].startswith(today_date):
            print(f"  {period['name']}: {period['detailedForecast']}")
            print( period )


    
forecast_data = get_forecast_data(api_endpoint, latitude, longitude)
render_forecast_data( forecast_data)

draw_forecast( forecast_data)