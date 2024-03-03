import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

def get_weather_icon(icon_name):
    # Add your icon mapping here
    icon_mapping = {
        "clear": "sun.png",
        "cloudy": "cloud.png",
        "rain": "rain.png",
        "snow": "snow.png",
        "storm": "storm.png",
        "fog": "fog.png"
    }
    return icon_mapping.get(icon_name, "unknown.png")

def display_weather_icon(api_endpoint, latitude, longitude):
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

            # Get the weather icon for the current conditions
            icon_name = forecast_data['properties']['periods'][0]['icon']
            icon_filename = get_weather_icon(icon_name)

            # Display the weather icon
            if icon_filename:
                icon_url = f"https://example.com/{icon_filename}"  # Replace with the actual URL of your icons
                icon_response = requests.get(icon_url)
                if icon_response.status_code == 200:
                    # Load the image and display it
                    img = Image.open(BytesIO(icon_response.content))
                    plt.imshow(img)
                    plt.axis('off')
                    plt.show()
                else:
                    print(f"Failed to fetch icon. Status code: {icon_response.status_code}")
            else:
                print("Icon not found for current conditions.")
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
display_weather_icon(api_endpoint, latitude, longitude)

