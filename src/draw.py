
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from datetime import datetime
import requests
from io import BytesIO

from ai import write_weather_poem



EPD_WIDTH = 264
EPD_HEIGHT = 176

megafont = ImageFont.truetype("./fonts/roboto/Roboto-Regular.ttf",  48)
mediumfont = ImageFont.truetype("./fonts/roboto/Roboto-Regular.ttf",  30)

smallfont = ImageFont.truetype("./fonts/roboto/Roboto-Regular.ttf",  20)


def draw_weather_poem(forecast_data):
    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the image with white
    image_red = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the image with white
    current_time = datetime.now().strftime('%I:%M %p')
    draw = ImageDraw.Draw(image)

    today_date = datetime.now().strftime('%Y-%m-%d')


    i = 0
    for period in forecast_data['properties']['periods']:
        if period['startTime'].startswith(today_date):
            print(f"  {period['name']}: {period['detailedForecast']}")
            print( period )

            if i == 0:
                detailedForecast = period['detailedForecast']
                text = write_weather_poem(detailedForecast)
                print(text)
        i = i+ 1

    draw.text( (10,10), text, font=smallfont, fill =0 )

    render_to_epaper(image, image_red)
    image.save("weatherpoem.bmp")


def draw_forecast( forecast_data ):
    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the image with white

    image_red = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the image with white
    draw_red = ImageDraw.Draw(image_red)

    draw = ImageDraw.Draw(image)
    today_date = datetime.now().strftime('%Y-%m-%d')

    


    i = 0
    for period in forecast_data['properties']['periods']:
        if period['startTime'].startswith(today_date):
            print(f"  {period['name']}: {period['detailedForecast']}")
            print( period )

            if i == 0:
                weather_icon_url = period['icon']
                response = requests.get(weather_icon_url)
                weather_icon = Image.open(BytesIO(response.content))
                image_red.paste(weather_icon, (EPD_WIDTH - weather_icon.width, int(EPD_HEIGHT/2)))


            draw.text((5, i * 40), period['name'], fill = 0)

            detailed_forecast_lines = period['detailedForecast'].split('. ', 1)
            for j, line in enumerate(detailed_forecast_lines):
                if line:  # Check if line is not empty


                    draw.text((15, i * 40 + 10 + (j * 10)), line + ('.' if j == 0 else ''), fill = 0)


            if i==0:
                draw.text((15, 110 ), str(period['temperature']), fill =0, font=megafont )

                draw.text((70, 125 ), str(period['shortForecast']), fill =0, font=mediumfont )

            i = i + 1

    # # https://github.com/waveshareteam/e-Paper/blob/60762ac5a3787ca7c3080d0e1f256a32ec3147e6/RaspberryPi_JetsonNano/python/examples/epd_2in7_test.py
    
    # render_to_epaper(image, image_red)

    image.save("output.bmp")


# import epaper
def render_to_epaper( image_black, image_red= None):
    epd = epaper.epaper('epd2in7b').EPD()

    epd.init()

    if image_red == None:
        epd.display(epd.getbuffer(image_black))
    else: 
        epd.display(epd.getbuffer(image_black), epd.getbuffer(image_red))

