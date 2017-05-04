import sys
import time
from time import localtime, strftime, gmtime
from pytz import timezone
from datetime import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from sysInfo.sysInfo import SysInfo
from etc.style import *

REFRESH_RATE_FAST = 900
REFRESH_RATE_MEDIUM = 5000
REFRESH_RATE_SLOW = 30000

day = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(qApp.quit)
        self.setContextMenu(menu)

class Window(QMainWindow):
    def __init__(self, x, y, w, h, parent = None):
        super(Window, self).__init__(parent)

        self.sys = SysInfo()
        self.modules = SETTINGS.get("SysMonitor", "modules").split(",")
        self.initUI(x, y, w, h)

    def initUI(self, x, y, w, h):
        self.win        = QFrame()
        self.mainVBox   = QVBoxLayout()
        self.timer      = QTimer()

        self.mainVBox.setSpacing(0)
        self.mainVBox.setContentsMargins(10, 10, 10, 10)
        self.win.setLayout(self.mainVBox)
        self.setCentralWidget(self.win)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.setGeometry(x, y, w, h)

        self.setStyleSheet(STYLE_BACKGROUND)
        self.win.setStyleSheet("QFrame{color:" + COLOR_TEXT + ";}" + STYLE_PROGRESSBAR)

        self.fillUI()
        self.show()

        self.timer.setInterval(900)
        self.timer.timeout.connect(self.updateUI)
        self.timer.start()

#        self.thread.started.connect(self.timer.start)
#        self.thread.finished.connect(self.updateUI)

    def fillUI(self):
        self.sys.update()

        #System Info
        if "SYSTEM" in self.modules:
            self.systemFrame    = QFrame()
            self.systemBox      = QGridLayout(self.systemFrame)

            self.topButton      = QPushButton("Toggle to above")
            self.topButton.setCheckable(True)
            self.topButton.clicked.connect(self.setFlags)
            self.propButton     = QPushButton("Show Properties")
            self.propButton.clicked.connect(self.showProperties)
            self.time           = QLabel()
            self.user           = QLabel()

            self.time.setText(color(bold(day[datetime.today().weekday()] + strftime(":  %d-%m-%Y  %H:%M:%S",
                localtime())), COLOR_EXTRA))
            self.user.setText(color(bold(str(self.sys.USER_user())) + color(" up since ", COLOR_TEXT)
                + bold(strftime("%H:%M", localtime(self.sys.USER_uptime()))), COLOR_EXTRA))

            self.systemBox.addWidget(self.topButton, 0, 0, 1, 3, Qt.AlignCenter)
            self.systemBox.addWidget(self.propButton, 1, 0, 1, 3, Qt.AlignCenter)
            self.systemBox.addWidget(QLabel(color(bold(self.sys.osName), COLOR_SYSTEM)), 2, 0, 1, 3, Qt.AlignCenter)
            self.systemBox.addWidget(QLabel(color(bold(self.sys.osArchitecture), COLOR_SYSTEM)), 3, 0, 1, 3, Qt.AlignCenter)
            self.systemBox.addWidget(self.time, 4, 0, 1, 3, Qt.AlignCenter)
            self.systemBox.addWidget(self.user, 5, 0, 1, 3, Qt.AlignCenter)

            self.systemFrame.setStyleSheet(STYLE_FRAME + STYLE_BUTTON)
            self.systemBox.setSpacing(0)
            self.systemBox.setContentsMargins(0, 0, 0, 0)

        #CPU Info
        if "CPU" in self.modules:
            self.cpuFrame       = QFrame()
            self.cpuBox         = QGridLayout(self.cpuFrame)
            self.cpu            = [None] * 4
            self.cpuBar         = [None] * 4

            self.cpuBox.addWidget(QLabel(color(bold("CPU"), COLOR_HEADER)), 0, 0, 1, 4, Qt.AlignCenter)

            for i in range(0, self.sys.cpus):
                self.cpu[i]     = QLabel(color(str(self.sys.CPU_temp(i)) + " " + u'\N{DEGREE SIGN}' + "C", COLOR_VALUE))
                self.cpuBar[i]  = QProgressBar()
                self.cpuBar[i].setTextVisible(False)

                self.cpuBox.addWidget(QLabel(bold("CPU " + str(i))), i + 1, 0)
                self.cpuBox.addWidget(self.cpuBar[i], i + 1, 1, 1, 2, Qt.AlignCenter)
                self.cpuBox.addWidget(self.cpu[i], i + 1, 3, 1, 1, Qt.AlignRight)

            self.cpuFrame.setStyleSheet(STYLE_FRAME + STYLE_PROGRESSBAR)
            self.cpuBox.setSpacing(0)
            self.cpuBox.setContentsMargins(0, 0, 0, 0)

        #GPU Info
        if "GPU" in self.modules:
            self.gpuFrame       = QFrame()
            self.gpuBox         = QGridLayout(self.gpuFrame)

            self.gpuname = QLabel(color(bold("NO GRAPHICS CARD"), COLOR_SYSTEM))
            self.gputemp = QLabel(color(str(0) + " " + u'\N{DEGREE SIGN}' + "C", COLOR_VALUE))
            self.gpugpu  = QLabel(color(italic(str(0) + " %"), COLOR_VALUE))
            self.gpufan  = QLabel(color(italic(str(0) + " %"), COLOR_VALUE))
            self.gpuram  = QLabel(color(italic(str(0) + " %"), COLOR_VALUE))
            self.gputotal= QLabel(color(str(0) + " MB", COLOR_VALUE))
            self.gpuused = QLabel(color(bold("used: "), COLOR_TEXT) + color(str(0) + " MB", COLOR_VALUE))
            self.gpufree = QLabel(color(bold("free: "), COLOR_TEXT) + color(str(0) + " MB", COLOR_VALUE))

            if self.sys.gpuType == 1:
                self.gpuname = QLabel(color(self.sys.GPU_name(), COLOR_VALUE))
                self.gputemp = QLabel(color(str(self.sys.GPU_temp()) + " " + u'\N{DEGREE SIGN}' + "C", COLOR_VALUE))
                self.gpugpu  = QLabel(color(italic(str(self.sys.GPU_usage_gpu()) + " %"), COLOR_VALUE))
                self.gpufan  = QLabel(color(italic(str(self.sys.GPU_usage_fan()) + " %"), COLOR_VALUE))
                self.gpuram  = QLabel(color(italic(str(self.sys.GPU_usage_mem()) + " %"), COLOR_VALUE))
                self.gputotal= QLabel(color(str(self.sys.GPU_MEM_total()) + " MB", COLOR_VALUE))
                self.gpuused = QLabel(color(bold("used: "), COLOR_TEXT) + color(str(self.sys.GPU_MEM_used()) + " MB", COLOR_VALUE))
                self.gpufree = QLabel(color(bold("free: "), COLOR_TEXT) + color(str(self.sys.GPU_MEM_free()) + " MB", COLOR_VALUE))

            self.gpubar = QProgressBar()
            self.gpubar.setTextVisible(False)
            self.gpufanbar = QProgressBar()
            self.gpufanbar.setTextVisible(False)
            self.gpurambar = QProgressBar()
            self.gpurambar.setTextVisible(False)
            self.gpurambar.setRange(0, self.sys.GPU_MEM_total())

            self.gpuBox.addWidget(QLabel(color(bold("GPU"), COLOR_HEADER)), 0, 0, 1, 4, Qt.AlignCenter)
            self.gpuBox.addWidget(QLabel(bold("Name")), 1, 0)
            self.gpuBox.addWidget(self.gpuname, 1, 1, 1, 2, Qt.AlignCenter)
            self.gpuBox.addWidget(QLabel(bold("GPU")), 2, 0)
            self.gpuBox.addWidget(self.gpubar, 2, 1, 1, 2, Qt.AlignCenter)
            self.gpuBox.addWidget(self.gpugpu, 2, 3, 1, 1, Qt.AlignRight)
            self.gpuBox.addWidget(QLabel(bold("FAN")), 3, 0)
            self.gpuBox.addWidget(self.gpufanbar, 3, 1, 1, 2, Qt.AlignCenter)
            self.gpuBox.addWidget(self.gpufan, 3, 3, 1, 1, Qt.AlignRight)
            self.gpuBox.addWidget(QLabel(bold("RAM")), 4, 0)
            self.gpuBox.addWidget(self.gpurambar, 4, 1, 1, 2, Qt.AlignCenter)
            self.gpuBox.addWidget(self.gputotal, 4, 3, 1, 1, Qt.AlignRight)
            self.gpuBox.addWidget(self.gputemp, 5, 0, 1, 1, Qt.AlignLeft)
            self.gpuBox.addWidget(self.gpuused, 5, 1, 1, 1, Qt.AlignLeft)
            self.gpuBox.addWidget(self.gpufree, 5, 2, 1, 2, Qt.AlignRight)

            self.gpuFrame.setStyleSheet(STYLE_FRAME)
            self.gpuBox.setSpacing(0)
            self.gpuBox.setContentsMargins(0, 0, 0, 0)

        #RAM Info
        if "RAM" in self.modules:
            self.ramFrame       = QFrame()
            self.ramBox         = QGridLayout(self.ramFrame)

            self.ramtotal = QLabel(color(str(self.sys.RAM_total()) + " MB", COLOR_VALUE))
            self.ramused  = QLabel(color(bold("used: "), COLOR_TEXT) + color(str(self.sys.RAM_usage_total()) + " MB", COLOR_VALUE))
            self.ramfree  = QLabel(color(bold("free: "), COLOR_TEXT) + color(str(self.sys.RAM_free()) + " MB", COLOR_VALUE))

            self.rambar = QProgressBar()
            self.rambar.setTextVisible(False)
            self.rambar.setRange(0, self.sys.RAM_total())
            self.rambar.setValue(self.sys.RAM_usage_total())

            self.ramBox.addWidget(QLabel(color(bold("RAM"), COLOR_HEADER)), 0, 0, 1, 4, Qt.AlignCenter)
            self.ramBox.addWidget(QLabel(bold("usage")), 1, 0)
            self.ramBox.addWidget(self.rambar, 1, 1, 1, 2, Qt.AlignCenter)
            self.ramBox.addWidget(self.ramtotal, 1, 3, 1, 1, Qt.AlignRight)
            self.ramBox.addWidget(self.ramused, 2, 1, 1, 1, Qt.AlignLeft)
            self.ramBox.addWidget(self.ramfree, 2, 2, 1, 2, Qt.AlignRight)
            self.ramBox.addWidget(QLabel(""), 3, 0, 1, 4)
            self.ramBox.addWidget(QLabel(""), 4, 0, 1, 4)

            self.ramFrame.setStyleSheet(STYLE_FRAME + STYLE_PROGRESSBAR)
            self.ramBox.setSpacing(0)
            self.ramBox.setContentsMargins(0, 0, 0, 0)

        #SWAP Info
        if "SWAP" in self.modules:
            self.swapFrame      = QFrame()
            self.swapBox        = QGridLayout(self.swapFrame)

            self.swaptotal = QLabel(color(str(self.sys.SWAP_total()) + " MB", COLOR_VALUE))
            self.swapused  = QLabel(color(bold("used: "), COLOR_TEXT) + color(str(self.sys.SWAP_usage_total())+" MB", COLOR_VALUE))
            self.swapfree  = QLabel(color(bold("free: "), COLOR_TEXT) + color(str(self.sys.SWAP_free())+" MB", COLOR_VALUE))

            self.swapbar = QProgressBar()
            self.swapbar.setTextVisible(False)
            self.swapbar.setRange(0, self.sys.SWAP_total())
            self.swapbar.setValue(self.sys.SWAP_usage_total())

            self.swapBox.addWidget(QLabel(color(bold("SWAP"), COLOR_HEADER)), 0, 0, 1, 4, Qt.AlignCenter)
            self.swapBox.addWidget(QLabel(bold("usage")), 1, 0)
            self.swapBox.addWidget(self.swapbar, 1, 1, 1, 2, Qt.AlignCenter)
            self.swapBox.addWidget(self.swaptotal, 1, 3, 1, 1, Qt.AlignRight)
            self.swapBox.addWidget(self.swapused, 2, 1, 1, 1, Qt.AlignLeft)
            self.swapBox.addWidget(self.swapfree, 2, 2, 1, 2, Qt.AlignRight)
            self.swapBox.addWidget(QLabel(""), 3, 0, 1, 4)
            self.swapBox.addWidget(QLabel(""), 4, 0, 1, 4)

            self.swapFrame.setStyleSheet(STYLE_FRAME + STYLE_PROGRESSBAR)
            self.swapBox.setSpacing(0)
            self.swapBox.setContentsMargins(0, 0, 0, 0)

        #DISK Info
        if "DISK" in self.modules:
            self.diskTab    = QTabWidget()
            self.diskFrame  = [0] * len(self.sys.disks)
            self.disktemp   = [0] * len(self.sys.disks)
            self.diskbar    = [0] * len(self.sys.disks)

            for i in range(0, len(self.sys.disks)):
                if self.sys.disk[i]:
                    self.diskFrame[i]   = QFrame()
                    self.diskBox        = QGridLayout(self.diskFrame[i])

                    self.disktotal      = QLabel(color(str(self.sys.DISK_total(i)) + " GB", COLOR_VALUE))
                    self.disktemp[i]    = QLabel(color(str(self.sys.DISK_temp(i)) + u'\N{DEGREE SIGN}' + "C", COLOR_VALUE))
                    self.diskused       = QLabel(color(bold("used: "), COLOR_TEXT) + color(str(self.sys.DISK_usage_total(i)) + " GB", COLOR_VALUE))
                    self.diskfree       = QLabel(color(bold("free: "), COLOR_TEXT) + color(str(self.sys.DISK_free(i)) + " GB", COLOR_VALUE))


                    self.diskbar[i] = QProgressBar()
                    self.diskbar[i].setTextVisible(False)
                    self.diskbar[i].setRange(0, self.sys.DISK_total(i))
                    self.diskbar[i].setValue(self.sys.DISK_usage_total(i))

                    self.diskBox.addWidget(QLabel(color(bold("DISK"), COLOR_HEADER)), 0, 0, 1, 4, Qt.AlignCenter)
                    self.diskBox.addWidget(QLabel(bold("usage")), 1, 0)
                    self.diskBox.addWidget(self.diskbar[i], 1, 1, 1, 2, Qt.AlignCenter)
                    self.diskBox.addWidget(self.disktotal, 1, 3, 1, 1, Qt.AlignRight)
                    self.diskBox.addWidget(self.disktemp[i], 2, 0, 1, 1, Qt.AlignLeft)
                    self.diskBox.addWidget(self.diskused, 2, 1, 1, 1, Qt.AlignLeft)
                    self.diskBox.addWidget(self.diskfree, 2, 2, 1, 2, Qt.AlignRight)
                    self.diskBox.addWidget(QLabel(""), 3, 0, 1, 4)
                    self.diskBox.addWidget(QLabel(""), 4, 0, 1, 4)

                    self.diskBox.setSpacing(0)
                    self.diskBox.setContentsMargins(0, 0, 0, 0)

                    self.diskFrame[i].setStyleSheet(STYLE_FRAME + STYLE_PROGRESSBAR)

                    self.diskTab.addTab(self.diskFrame[i], self.sys.drive[i])

            self.diskTab.setStyleSheet(STYLE_ALL)

        #NET Info
        if "NET" in self.modules:
            self.netTab         = QTabWidget()
            self.netFrame       = [0] * len(self.sys.nets)
            self.netName        = [0] * len(self.sys.nets)
            self.netaddress     = [0] * len(self.sys.nets)
            self.netupspeed     = [0] * len(self.sys.nets)
            self.netdownspeed   = [0] * len(self.sys.nets)

            for i,net in enumerate(self.sys.nets):
                self.netFrame[i]    = QWidget()
                self.netBox         = QGridLayout(self.netFrame[i])

                self.netName[i]      = self.sys.NET_name(net)
                self.netname         = QLabel(color(self.sys.NET_name(net), COLOR_VALUE))
                self.netaddress[i]   = QLabel(color(self.sys.NET_address(net), COLOR_VALUE))
                self.netupGraph      = QLabel("")
                self.netdownGraph    = QLabel("")
                self.netupspeed[i]   = QLabel(color(str(self.sys.NET_upspeed(net)) + " kB/s", COLOR_VALUE))
                self.netdownspeed[i] = QLabel(color(str(self.sys.NET_downspeed(net)) + " kB/s", COLOR_VALUE))

                self.netBox.addWidget(QLabel(color(bold("NET"), COLOR_HEADER)), 0, 0, 1, 3, Qt.AlignCenter)
                self.netBox.addWidget(QLabel(bold("Name")), 1, 0)
                self.netBox.addWidget(self.netname, 1, 1, 1, 2, Qt.AlignRight)
                self.netBox.addWidget(QLabel(bold("IP")), 2, 0)
                self.netBox.addWidget(self.netaddress[i], 2, 1, 1, 2, Qt.AlignRight)
                self.netBox.addWidget(QLabel(bold("up")), 3, 0)
                self.netBox.addWidget(self.netupGraph, 3, 1, 1, 1, Qt.AlignCenter)
                self.netBox.addWidget(self.netupspeed[i], 3, 2, 1, 1, Qt.AlignRight)
                self.netBox.addWidget(QLabel(bold("down")), 4, 0)
                self.netBox.addWidget(self.netdownGraph, 4, 1, 1, 1, Qt.AlignCenter)
                self.netBox.addWidget(self.netdownspeed[i], 4, 2, 1, 1, Qt.AlignRight)

                self.netBox.setSpacing(0)
                self.netBox.setContentsMargins(0, 0, 0, 0)

                self.netFrame[i].setStyleSheet(STYLE_FRAME + STYLE_PROGRESSBAR)

                self.netTab.addTab(self.netFrame[i], self.netName[i])

            self.netTab.setStyleSheet(STYLE_ALL)

        if "SYSTEM" in self.modules:
            self.mainVBox.addWidget(self.systemFrame)
        if "CPU" in self.modules:
            self.mainVBox.addWidget(self.cpuFrame)
        if "GPU" in self.modules:
            self.mainVBox.addWidget(self.gpuFrame)
        if "RAM" in self.modules:
            self.mainVBox.addWidget(self.ramFrame)
        if "SWAP" in self.modules:
            self.mainVBox.addWidget(self.swapFrame)
        if "DISK" in self.modules:
            if len(self.sys.disks) > 1:
                self.mainVBox.addWidget(self.diskTab)
            else:
                self.mainVBox.addWidget(self.diskFrame)
        if "NET" in self.modules:
            if len(self.sys.nets) > 1:
                self.mainVBox.addWidget(self.netTab)
            else:
                self.mainVBox.addWidget(self.netFrame)


    def updateUI(self):
        #Update Systembox
        if "SYSTEM" in self.modules:
            self.time.setText(color(bold(day[datetime.today().weekday()] + strftime(":  %d-%m-%Y  %H:%M:%S",
                localtime())), COLOR_EXTRA))

        #Update CPUbox
        if "CPU" in self.modules:
            self.sys.CPU()
            for i in range(0, self.sys.cpus):
                self.cpu[i].setText(color(str(self.sys.CPU_temp(i)) + " " + u'\N{DEGREE SIGN}' + "C", COLOR_VALUE))
                self.cpuBar[i].setValue(self.sys.CPU_usage(i))

        #Update GPUbox
        if "GPU" in self.modules:
            self.sys.GPU()
            if self.sys.gpuType < 2:
                self.gpubar.setValue(self.sys.GPU_usage_gpu())
                self.gpufanbar.setValue(self.sys.GPU_usage_fan())
                self.gpurambar.setValue(self.sys.GPU_MEM_used())

                self.gpugpu.setText(color(italic(str(self.sys.GPU_usage_gpu()) + " %"), COLOR_VALUE))
                self.gpufan.setText(color(italic(str(self.sys.GPU_usage_fan()) + " %"), COLOR_VALUE))
                self.gpuram.setText(color(italic(str(self.sys.GPU_usage_mem()) + " %"), COLOR_VALUE))
                self.gputemp.setText(color(str(self.sys.GPU_temp()) + " " + u'\N{DEGREE SIGN}' + "C", COLOR_VALUE))
                self.gpuused.setText(color(bold("used: "), COLOR_TEXT) + color(str(self.sys.GPU_MEM_used()) + " MB", COLOR_VALUE))
                self.gpufree.setText(color(bold("free: "), COLOR_TEXT) + color(str(self.sys.GPU_MEM_free()) + " MB", COLOR_VALUE))

        #Update RAMbox
        if "RAM" in self.modules:
            self.sys.RAM()
            self.rambar.setValue(self.sys.RAM_usage_total())
            self.ramused.setText(color(bold("used: "), COLOR_TEXT) + color(str(self.sys.RAM_usage_total())+" MB", COLOR_VALUE))
            self.ramfree.setText(color(bold("free: "), COLOR_TEXT) + color(str(self.sys.RAM_free())+" MB", COLOR_VALUE))

        #Update SWAPbox
        if "SWAP" in self.modules:
            self.sys.SWAP()
            self.swapbar.setValue(self.sys.SWAP_usage_total())
            self.swapused.setText(color(bold("used: "), COLOR_TEXT) + color(str(self.sys.SWAP_usage_total())+" MB", COLOR_VALUE))
            self.swapfree.setText(color(bold("free: "), COLOR_TEXT) + color(str(self.sys.SWAP_free())+" MB", COLOR_VALUE))

        #Update NETbox
        if "NET" in self.modules:
            self.sys.NET()
            for i in range(0, len(self.sys.nets)):
                self.netupspeed[i].setText(color(str(self.sys.NET_upspeed("Ethernet")) + " kB/s", COLOR_VALUE))
                self.netdownspeed[i].setText(color(str(self.sys.NET_downspeed("Ethernet")) + " kB/s", COLOR_VALUE))


    def updateUIby5(self):
        self.sys.RAM()
        self.sys.SWAP()

        #Update RAMbox
        self.rambar.setValue(self.sys.RAM_usage_total())
        self.ramused.setText(color(bold("used: "), COLOR_TEXT) + color(str(self.sys.RAM_usage_total())+" MB", COLOR_VALUE))
        self.ramfree.setText(color(bold("free: "), COLOR_TEXT) + color(str(self.sys.RAM_free())+" MB", COLOR_VALUE))

        #Update SWAPbox
        self.swapbar.setValue(self.sys.SWAP_usage_total())
        self.swapused.setText(color(bold("used: "), COLOR_TEXT) + color(str(self.sys.SWAP_usage_total())+" MB", COLOR_VALUE))
        self.swapfree.setText(color(bold("free: "), COLOR_TEXT) + color(str(self.sys.SWAP_free())+" MB", COLOR_VALUE))

    def updateUIby30(self):
        self.sys.DISK()

        #Update DISKbox
        for i in range(0, len(self.sys.disks)):
            self.disktemp[i].setText(color(str(self.sys.DISK_temp(i)) + u'\N{DEGREE SIGN}' + "C", COLOR_VALUE))
            self.diskbar[i].setValue(self.sys.DISK_usage_total(i))

    def showProperties(self):
        self.propFrame  = QFrame()
        self.propBox    = QGridLayout(self.propFrame)

        self.propCPU    = QLabel(color(str(self.sys.cpus), COLOR_VALUE))
        self.propGPU    = QLabel(color(self.sys.GPU_name(), COLOR_VALUE))

        self.propBox.addWidget(QLabel(color(bold("CPU's:"), COLOR_TEXT)), 1, 0, 1, 1, Qt.AlignLeft)
        self.propBox.addWidget(self.propCPU, 1, 1, 1, 1, Qt.AlignRight)
        self.propBox.addWidget(QLabel(color(bold("GPU:"), COLOR_TEXT)), 2, 0, 1, 1, Qt.AlignLeft)
        self.propBox.addWidget(self.propGPU, 2, 1, 1, 1, Qt.AlignRight)
        self.propFrame.setStyleSheet(STYLE_BACKGROUND)

        self.propFrame.show()

    def setFlags(self):
        if self.topButton.isChecked():
            self.topButton.setText("Toggle to under")
            self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.topButton.setText("Toggle to above")
            self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
            self.show()

def bold(text):
    return "<b>" + text + "</b>"

def italic(text):
    return "<i>" + text + "</i>"

def color(text, color):
    return "<font color='" + color + "'>" + text + "</font>"