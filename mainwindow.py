
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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.meters = []
        with open('meters.txt') as f:
            for line in f:
                rawmeter = line.strip()
                if rawmeter:
                    meter = rawmeter[:12].zfill(12)
                    self.meters.append(meter)
                    self.ui.treeWidget.addTopLevelItem(
                        QTreeWidgetItem(None, [meter, '']))
        
        self.ui.comboBox_port.addItems([i[0] for i in comports()])
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.txtimer = QTimer(self)
        self.txtimer.timeout.connect(self.send)
        self.txtimer. setSingleShot(True)
        self.ser = None
        self.buf = bytearray()
        self.pktidx = [0]
        self.dstmeters = self.meters
        
    def update(self):
        if serial.VERSION == '2.7':
            inwaiting = self.ser.inWaiting()
        else:
            inwaiting = self.ser.in_waiting
        if inwaiting:
            self.buf.extend(self.ser.read(inwaiting))
            #print(self.buf)
            i = self.buf.find(b'\xFE\xFE\xFE\xFE')
            if i != -1:
                # from wl, no crc.
                if len(self.buf) > i+4 and len(self.buf)>= i + self.buf[i+4] + 5 +2:
                    #print(' '.join('%02X'%ii for ii in self.buf[i+8: i+self.buf[i+4]+5]))
                    try:
                        baseinfo, extinfo = PacketParser(self.buf[i+8: i+self.buf[i+4]+5])
                        #print(baseinfo)
                        #print(extinfo)
                        if baseinfo[4] == self.ui.lineEdit_localaddr.text().strip() and baseinfo[0] == 'aRoute':
                            self.ui.treeWidget.topLevelItem(self.meters.index(baseinfo[5])).setText(1, extinfo['data'])
                            if self.ui.pushButton_start.text() == '停止抄表' and baseinfo[5] == self.dstmeters[self.i]:
                                self.retry = self.ui.spinBox_retry.value()
                                self.ui.progressBar.setValue(self.i*3+self.retry)
                                self.txtimer.start(0)
                    except:
                        pass
                    del self.buf[: i+self.buf[i+4]+5+2]
 
    def send(self):
        if self.retry == self.ui.spinBox_retry.value():
            self.retry = 0
            self.i += 1
            if self.i == len(self.dstmeters):
                self.ui.pushButton_start.setText('开始抄表')
                self.ui.label_curmeter.setText('------------')
                self.ui.label_retry.setText('0')
                return
        meter = self.dstmeters[self.i]
        if self.ui.checkBox_nodata.isChecked() and \
                self.ui.treeWidget.topLevelItem(self.meters.index(meter)).text(1):
            self.retry = self.ui.spinBox_retry.value()
            self.ui.progressBar.setValue(self.i*3+self.retry)
            self.txtimer.start(0)
            return
        self.read_meter(meter)
        self.ui.label_curmeter.setText(meter)
        self.retry += 1
        self.ui.label_retry.setText(str(self.retry))
        self.ui.progressBar.setValue(self.i*3+self.retry)
        self.txtimer.start(self.ui.spinBox_interval.value() * 1000) 
 
    def read_meter(self, meter):
        dstaddr = bytearray.fromhex(meter)
        dstaddr.reverse()
        srcaddr = bytearray.fromhex(self.ui.lineEdit_localaddr.text())
        srcaddr.reverse()
        pkt = bytearray.fromhex(
            'FE FE FE FE 25 00 01 24 '
            '41 CD 5E FF FF 80 24 59 01 00 14 88 00 00 00 10 00 '
            '3C 80 24 59 01 00 14 AA AA AA AA AA AA 11 02 13 00 ')
        pkt[10] = self.pktidx[0] # mac index.
        pkt[13:19] = dstaddr
        pkt[19:25] = srcaddr
        pkt[26:32] = dstaddr
        pkt[32:38] = srcaddr
        pkt[38] = (pkt[38] & 0x0F) + ((self.pktidx[0] % 16) << 4) # nwk index.
        pkt[40] = self.i % 0x100 # aps index.
        pkt645 = bytearray.fromhex(self.ui.lineEdit_pkt645.text())
        pkt645[1:7] = dstaddr
        pkt645[-2] = sum(pkt645[:-2]) % 0x100
        pkt.extend(pkt645)
        pkt[4] = len(pkt) - 5
        pkt[5] = int(self.ui.comboBox_chnlgrp.currentText())*2 + int(self.ui.comboBox_chnl.currentText())
        pkt[7] = pkt[4] ^ pkt[5] ^ pkt[6]
        self.ser.write(pkt)
        self.pktidx[0] += 1
        if self.pktidx[0] > 255:
            self.pktidx[0] = 0

    @pyqtSlot()
    def on_pushButton_swithport_clicked(self):
        if self.ui.pushButton_swithport.text() == '打开':
            port = self.ui.comboBox_port.currentText()
            try:
                self.ser = serial.Serial(port, 115200, parity=serial.PARITY_EVEN, timeout=0)
                self.timer.start(1) 
                self.set_channel(int(self.ui.comboBox_chnlgrp.currentText()), int(self.ui.comboBox_chnl.currentText()))
                self.ui.pushButton_swithport.setText('关闭') 
            except:
                self.timer.stop()
                QMessageBox.warning(self, '警告', '无法打开 %s!' % port)
        else:
            self.ser.close()
            self.ser = None
            self.ui.pushButton_swithport.setText('打开')

    @pyqtSlot()
    def on_pushButton_start_clicked(self):
        if self.ui.pushButton_start.text() == '开始抄表':
            if self.ui.checkBox_selorall.isChecked():
                items = self.ui.treeWidget.selectedItems()
                if items:
                    self.dstmeters = [i.text(0) for i in items]
            else:
                self.dstmeters = self.meters
            self.ui.progressBar.setMaximum(len(self.dstmeters)*self.ui.spinBox_retry.value())
            if self.ser:
                self.i = 0
                self.retry = 0
                self.txtimer.start(0) 
                self.ui.pushButton_start.setText('停止抄表')
            else:
                QMessageBox.warning(self, '警告', '请先打开串口!')
        else:
            self.txtimer.stop()
            self.ui.pushButton_start.setText('开始抄表')
            
    def set_channel(self, chnlgrp,  chnl):
        pkt = bytearray.fromhex('FE FE FE FE 03 00 01 24')
        pkt[5] = chnlgrp*2 + chnl
        pkt[7] = pkt[4] ^ pkt[5] ^ pkt[6]
        if self.ser:
            self.ser.write(pkt)
        else:
            QMessageBox.warning(self, '警告', '请先打开串口!')
        
    @pyqtSlot(int)
    def on_comboBox_chnlgrp_currentIndexChanged(self, index):
        self.set_channel(index, int(self.ui.comboBox_chnl.currentText()))
        
    @pyqtSlot(int)
    def on_comboBox_chnl_currentIndexChanged(self, index):
        self.set_channel(int(self.ui.comboBox_chnlgrp.currentText()), index)

    @pyqtSlot()
    def on_pushButton_save_clicked(self):
        t = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        file = QFileDialog.getSaveFileName(self, 'Save file', './result/' + t, 'data file(*.txt)')[0]
        if file:
            with open(file, 'w') as f:
                for i in range(self.ui.treeWidget.topLevelItemCount()):
                    data = self.ui.treeWidget.topLevelItem(i).text(1)
                    if data:
                        meter = self.ui.treeWidget.topLevelItem(i).text(0)
                        f.write('%s, %s\n' % (meter, data))

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_itemDoubleClicked(self, item, column):
            if self.ser:
                self.i = self.ui.treeWidget.indexOfTopLevelItem(item)
                self.read_meter(item.text(0))
            else:
                QMessageBox.warning(self, '警告', '请先打开串口!')
