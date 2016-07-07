
import os.path
import pickle
from datetime import datetime
import traceback

from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QMenu, QFileDialog, QMessageBox#, QInputDialog
from PyQt5.QtGui import QBrush, QCursor
from PyQt5.QtCore import QTimer, pyqtSlot, Qt, QPoint

import serial
from serial.tools.list_ports import comports

from Ui_mainwindow import Ui_MainWindow

from packet import PacketParser
import upgrade
import rdebug

# known issue:
# 1, packet disp data error, when parse pkt disped.


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        with open('meters.txt') as f:
            for line in f:
                meter = line.strip()
                if meter:
                    self.ui.treeWidget.addTopLevelItem(
                        QTreeWidgetItem(None, [meter[:12].zfill(12), '']))
        self.ui.progressBar.setMaximum(self.ui.treeWidget.topLevelItemCount())
        
        self.ui.comboBox_port.addItems([i[0] for i in comports()])
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.ser = None
        self.buf = bytearray()
        
    def update(self):
#        try:
        if self.ser.in_waiting:
            self.buf.extend(self.ser.read(self.ser.in_waiting))
            i = self.buf.find(b'\xFE\xFE\xFE\xFE')
            if i != -1:
                # from wl, no crc.
                if len(self.buf) > i+4 and len(self.buf)>= i + self.buf[i+4] + 5:
                    baseinfo, extinfo = PacketParser(self.buf[i+8: i+self.buf[i+4]+5])
                    if baseinfo[0] == 'route':
                        pass
                    del self.buf[: i+self.buf[i+4]+5]
#        except:
#            with open('error.txt',  'a') as f:
#                f.write(traceback.format_exc())
        self.t += 1
        if self.t  == self.ui.spinBox_interval.value() * 10:
            self.t = 0
            meter = self.ui.treeWidget.topLevelItem(self.i).text(0)
            self.ui.label_curmeter.setText(meter)
            self.retry += 1
            self.ui.label_retry.setText(str(self.retry))
            if self.retry == self.ui.spinBox_retry.value():
                self.retry = 0
                self.i += 1
                if self.i == self.ui.treeWidget.topLevelItemCount():
                    self.on_pushButton_start_clicked()

    @pyqtSlot()
    def on_pushButton_swithport_clicked(self):
        if self.ui.pushButton_swithport.text() == '打开':
            port = self.ui.comboBox_port.currentText()
            try:
                self.ser = serial.Serial(port, 38400, timeout=0)
                self.ui.pushButton_swithport.setText('关闭') 
            except:
                QMessageBox.warning(self, '警告', '无法打开 %s!' % port)
        else:
            self.ser.close()
            self.ser = None
            self.ui.pushButton_swithport.setText('打开')

    @pyqtSlot()
    def on_pushButton_start_clicked(self):
        if self.ui.pushButton_start.text() == '开始抄表':
            if self.ser:
                self.t = 0
                self.i = 0
                self.retry = 0
                self.timer.start(100) 
                self.ui.pushButton_start.setText('停止抄表')
            else:
                QMessageBox.warning(self, '警告', '请先打开串口!')
        else:
            self.timer.stop()
            self.ui.pushButton_start.setText('开始抄表')
