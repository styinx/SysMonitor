# SysMonitor

![Example](https://github.com/styinx/SysMonitor/example.png)
___

## Development
**Dependencies:**

Software:
Python 3.4
To get SysMonitor running you need the PyQt5 development environment for python 3.4.
SysMonitor uses [OpenHardwaremonitor](http://openhardwaremonitor.org/) to collect temperature data from the hardware.

Python Modules:
psutil
pytz
PyQt5
wmi
___

## Installation

python -m PyInstaller --onefile --noconsole --windowed --icon=app.ico SysMonitor.py
___

## Issues

- Timer blocks UI interaction

___