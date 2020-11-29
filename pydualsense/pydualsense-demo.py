from PyQt5 import QtCore, QtGui, QtWidgets 
import sys 
from interface import Ui_MainWindow
from pydualsense import pydualsense

def colorR(value):
    global colorR
    colorR = value

def colorG(value):
    global colorG
    colorG = value

def colorB(value):
    global colorB
    colorB = value

def send():
    ds.setColor(colorR, colorG, colorB)
    ds.sendReport()
if __name__ == "__main__":
    global ds
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ds = pydualsense()
    # connect interface to  
    ui.slider_r.valueChanged.connect(colorR)
    ui.slider_g.valueChanged.connect(colorG)
    ui.slider_b.valueChanged.connect(colorB)
    ui.pushButton.clicked.connect(send)
    MainWindow.show()
    sys.exit(app.exec_())