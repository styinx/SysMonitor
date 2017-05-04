# SysMonitor

This application shows information about CPU, GPU, RAM, SWAP, DISK and NET.
With a config file you can easily choose colors, position and modules of the monitor.

<img align="left" src="https://github.com/styinx/SysMonitor/blob/master/ex_0.png" width="120" height="540" alt="Example"/>
<img align="right" src="https://github.com/styinx/SysMonitor/blob/master/ex_1.png" width="250" height="426" alt="Example"/>
<img align="right" src="https://github.com/styinx/SysMonitor/blob/master/ex_3.png" width="125" height="490" alt="Example"/>
<img align="right" src="https://github.com/styinx/SysMonitor/blob/master/ex_2.png" width="250" height="254" alt="Example"/>

___

<img src="https://github.com/styinx/SysMonitor/blob/master/ex_4.png" width="960" height="512" alt="Example"/>
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