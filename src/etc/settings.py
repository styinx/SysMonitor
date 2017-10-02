import configparser, os
import sys

from PyQt5.QtCore import *

SETTINGS = configparser.ConfigParser()
SETTINGS.read("./config.ini")

def isValidRect(rect, x, y, w, h):
    if x >= 0 and x <= rect.width() and y >= 0 and y <= rect.height():
        if w <= rect.width() - x and h <= rect.height() - y:
            return True
        else:
            return False
    else:
        return False

def getRect(app_desktop):
    rect         = QRect()
    desktop      = app_desktop
    screens      = desktop.screenCount()
    
    alignment = SETTINGS.get("Display", "align")
    screen = int(SETTINGS.get("Display", "screen"))
    x = int(SETTINGS.get("Display", "x"))
    y = int(SETTINGS.get("Display", "y"))
    w = int(SETTINGS.get("Display", "w"))
    h = int(SETTINGS.get("Display", "h"))
    
    for arg in sys.argv:
        if "-align=" in arg:
            alignment = arg[7:]

        if "-screen=" in arg:
            screen = int(arg[8:])

        if "-x=" in arg:
            x = int(arg[3:])
 
        if "-y=" in arg:
            y = int(arg[3:])

        if "-w=" in arg:
            w = int(arg[3:])

        if "-h=" in arg:
            h = int(arg[3:])

    if x < 0:
        x = 0
    if y < 0:
        y = 0

    if screen != -1:
        if screen >= 0 and screen <= screens:
            if isValidRect(desktop.screenGeometry(screen), x, y, w, h):
                rect = desktop.screenGeometry(screen)
                rect = QRect(rect.x() + x, rect.y() + y, w, h)
    else:
        if alignment == "left" or alignment == "right":
            if alignment == "left":
                screen = 0
            else:
                screen = screens - 1

    if alignment == "left" or alignment == "right":
        if alignment == "left":
            x = desktop.screenGeometry(screen).x() + x
            rect = QRect(x, y, w, h)
        else:
            x = desktop.screenGeometry(screen).x() + x + desktop.screenGeometry(screen).width() - w
            rect = QRect(x, y, w, h)

    if h == -1:
        rect.setHeight(desktop.screenGeometry(screen).height())
    elif h < -1 and h >= desktop.screenGeometry(screen).height() * -1:
        rect.setHeight(desktop.screenGeometry(screen).height() + h)

    rect.setHeight(rect.height() - y)

    return rect