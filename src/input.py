from gpiozero import Button
from signal import pause

from ai import get_baltimore_forecast
from draw import draw_forecast, draw_clock

btn_1 = Button(5)
btn_2 = Button(6)
btn_3 = Button(13)
btn_4 = Button(19)

def handleButton1():    
    draw_forecast( get_baltimore_forecast())

    print(" button 1")

def handleButton2():
    draw_clock()
    print(" button 2")

def handleButton3():
    print(" button 3")

def handleButton4():
    print(" button 4")


def setupButtons():
    btn_1.when_pressed = handleButton1
    btn_2.when_pressed = handleButton2
    btn_3.when_pressed = handleButton3
    btn_4.when_pressed = handleButton4

    pause()

setupButtons()