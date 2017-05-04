from gui.gui import *

'''
#
#       This is the class which start the application
#
'''
class Application():
    def __init__(self, argv):
        self.app      = QApplication(argv)
        rect          = getRect(self.app.desktop())
        self.win      = Window(rect.x(), rect.y(), rect.width(), rect.height())
        self.trayIcon = SystemTrayIcon(QIcon("app.ico"), self.win)
        self.trayIcon.show()

    def __del__(self):
        self.trayIcon.hide()

if __name__ == "__main__":
    app = Application(sys.argv)
    sys.exit(app.app.exec_())