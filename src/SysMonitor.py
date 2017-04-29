import sys
from gui.gui import *

X = 0
Y = 0
W = 240
Ho = 40

# Widget will be placed in the right side of the screen
# If 2 or more monitors are connected, it will be assumed
# that only the left desktop has a taskbar !(Windows)!
class Application():
    def __init__(self, argv):
        self.app = QApplication(argv)
        desktop = self.app.desktop()

        screens = desktop.screenCount()

        self.x = desktop.screen(0).width() - W
        self.h = desktop.screen(0).height() - Ho

        if screens > 1:
            for i in range(1, screens):
                self.x += desktop.screen(i).width()
            self.h = desktop.screen(screens - 1).height()

        self.y = Y
        self.w = W

        self.win = Window(self.x, self.y, self.w, self.h)
        self.trayIcon = SystemTrayIcon(QIcon("app.ico"), self.win)
        self.trayIcon.show()

    def __del__(self):
        self.trayIcon.hide()

if __name__ == "__main__":
    app = Application(sys.argv)
    sys.exit(app.app.exec_())