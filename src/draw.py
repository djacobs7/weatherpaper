
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from datetime import datetime
import requests
from io import BytesIO




EPD_WIDTH = 264
EPD_HEIGHT = 176

def draw_forecast( forecast_data ):
    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the image with white

    image_red = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the image with white
    draw_red = ImageDraw.Draw(image_red)

    draw = ImageDraw.Draw(image)
    # font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18)
    today_date = datetime.now().strftime('%Y-%m-%d')


    # Download the image


    # Add the image to the drawing
    
    megafont = ImageFont.truetype("./fonts/roboto/Roboto-Regular.ttf",  48)

    mediumfont = ImageFont.truetype("./fonts/roboto/Roboto-Regular.ttf",  30)


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


    # draw.rectangle((0, 76, 176, 96), fill = 0)
    # # draw.text((18, 80), 'Hello world!', font = font, fill = 255)
    # draw.line((10, 130, 10, 180), fill = 0)
    # draw.line((10, 130, 50, 130), fill = 0)
    # draw.line((50, 130, 50, 180), fill = 0)
    # draw.line((10, 180, 50, 180), fill = 0)
    # draw.line((10, 130, 50, 180), fill = 0)
    # draw.line((50, 130, 10, 180), fill = 0)
    # draw.arc((90, 190, 150, 250), 0, 360, fill = 0)
    # draw.chord((90, 120, 150, 180), 0, 360, fill = 0)
    # draw.rectangle((10, 200, 50, 250), fill = 0)




    # # https://github.com/waveshareteam/e-Paper/blob/60762ac5a3787ca7c3080d0e1f256a32ec3147e6/RaspberryPi_JetsonNano/python/examples/epd_2in7_test.py
    
    render_to_epaper(image, image_red)

    image.save("output.bmp")


import epaper
def render_to_epaper( image_black, image_red ):
    epd = epaper.epaper('epd2in7b').EPD()

    epd.init()
    epd.display(epd.getbuffer(image_black), epd.getbuffer(image_red))


# HOW TO MAKE THE BUTTONS DO STUDD
#https://dev.to/ranewallin/getting-started-with-the-waveshare-2-7-epaper-hat-on-raspberry-pi-41m8