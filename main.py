
import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow


version = '0.1.0'


if __name__ == '__main__':    
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    
    sys.exit(app.exec_())
