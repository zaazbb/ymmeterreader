# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\work\repository\ymmeterreader\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.comboBox_port = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_port.setEditable(True)
        self.comboBox_port.setObjectName("comboBox_port")
        self.horizontalLayout_3.addWidget(self.comboBox_port)
        self.pushButton_swithport = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_swithport.setObjectName("pushButton_swithport")
        self.horizontalLayout_3.addWidget(self.pushButton_swithport)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.lineEdit_localaddr = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_localaddr.setObjectName("lineEdit_localaddr")
        self.horizontalLayout_3.addWidget(self.lineEdit_localaddr)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9)
        self.comboBox_chnlgrp = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_chnlgrp.setObjectName("comboBox_chnlgrp")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox_chnlgrp)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_3.addWidget(self.label_11)
        self.comboBox_chnl = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_chnl.setObjectName("comboBox_chnl")
        self.comboBox_chnl.addItem("")
        self.comboBox_chnl.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox_chnl)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.spinBox_interval = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_interval.setMinimum(1)
        self.spinBox_interval.setMaximum(30)
        self.spinBox_interval.setObjectName("spinBox_interval")
        self.horizontalLayout_3.addWidget(self.spinBox_interval)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.spinBox_retry = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_retry.setMinimum(1)
        self.spinBox_retry.setMaximum(10)
        self.spinBox_retry.setProperty("value", 3)
        self.spinBox_retry.setObjectName("spinBox_retry")
        self.horizontalLayout_3.addWidget(self.spinBox_retry)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.lineEdit_pkt645 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_pkt645.setEnabled(False)
        self.lineEdit_pkt645.setObjectName("lineEdit_pkt645")
        self.horizontalLayout.addWidget(self.lineEdit_pkt645)
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout.addWidget(self.label_12)
        self.spinBox_round = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_round.setMinimum(1)
        self.spinBox_round.setMaximum(99)
        self.spinBox_round.setObjectName("spinBox_round")
        self.horizontalLayout.addWidget(self.spinBox_round)
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout.addWidget(self.label_13)
        self.spinBox_okrate = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_okrate.setMinimum(1)
        self.spinBox_okrate.setMaximum(100)
        self.spinBox_okrate.setProperty("value", 90)
        self.spinBox_okrate.setObjectName("spinBox_okrate")
        self.horizontalLayout.addWidget(self.spinBox_okrate)
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout.addWidget(self.label_14)
        self.pushButton_start = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayout.addWidget(self.pushButton_start)
        self.pushButton_save = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout.addWidget(self.pushButton_save)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.treeWidget = QtWidgets.QTreeWidget(self.centralWidget)
        self.treeWidget.setIndentation(0)
        self.treeWidget.setObjectName("treeWidget")
        self.verticalLayout_2.addWidget(self.treeWidget)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_2)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.label_15 = QtWidgets.QLabel(self.groupBox_2)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_2.addWidget(self.label_15)
        self.label_curround = QtWidgets.QLabel(self.groupBox_2)
        self.label_curround.setObjectName("label_curround")
        self.horizontalLayout_2.addWidget(self.label_curround)
        self.label_17 = QtWidgets.QLabel(self.groupBox_2)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_2.addWidget(self.label_17)
        self.label_currate = QtWidgets.QLabel(self.groupBox_2)
        self.label_currate.setObjectName("label_currate")
        self.horizontalLayout_2.addWidget(self.label_currate)
        self.label_currate_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_currate_2.setObjectName("label_currate_2")
        self.horizontalLayout_2.addWidget(self.label_currate_2)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.label_curmeter = QtWidgets.QLabel(self.groupBox_2)
        self.label_curmeter.setObjectName("label_curmeter")
        self.horizontalLayout_2.addWidget(self.label_curmeter)
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.label_retry = QtWidgets.QLabel(self.groupBox_2)
        self.label_retry.setObjectName("label_retry")
        self.horizontalLayout_2.addWidget(self.label_retry)
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        self.horizontalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        MainWindow.setCentralWidget(self.centralWidget)
        self.actionSaveAs = QtWidgets.QAction(MainWindow)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionUpgBpSts = QtWidgets.QAction(MainWindow)
        self.actionUpgBpSts.setObjectName("actionUpgBpSts")
        self.actionUpgTxm = QtWidgets.QAction(MainWindow)
        self.actionUpgTxm.setObjectName("actionUpgTxm")
        self.actionRdSnCfg = QtWidgets.QAction(MainWindow)
        self.actionRdSnCfg.setObjectName("actionRdSnCfg")
        self.actionUpgRdBack = QtWidgets.QAction(MainWindow)
        self.actionUpgRdBack.setObjectName("actionUpgRdBack")
        self.actionRmParsed = QtWidgets.QAction(MainWindow)
        self.actionRmParsed.setObjectName("actionRmParsed")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "抄表软件"))
        self.groupBox.setTitle(_translate("MainWindow", "配置"))
        self.label.setText(_translate("MainWindow", "串口:"))
        self.pushButton_swithport.setText(_translate("MainWindow", "打开"))
        self.label_7.setText(_translate("MainWindow", "本地地址:"))
        self.lineEdit_localaddr.setText(_translate("MainWindow", "112233445566"))
        self.label_9.setText(_translate("MainWindow", "信道组:"))
        self.comboBox_chnlgrp.setItemText(0, _translate("MainWindow", "0"))
        self.comboBox_chnlgrp.setItemText(1, _translate("MainWindow", "1"))
        self.comboBox_chnlgrp.setItemText(2, _translate("MainWindow", "2"))
        self.comboBox_chnlgrp.setItemText(3, _translate("MainWindow", "3"))
        self.comboBox_chnlgrp.setItemText(4, _translate("MainWindow", "4"))
        self.comboBox_chnlgrp.setItemText(5, _translate("MainWindow", "5"))
        self.comboBox_chnlgrp.setItemText(6, _translate("MainWindow", "6"))
        self.comboBox_chnlgrp.setItemText(7, _translate("MainWindow", "7"))
        self.comboBox_chnlgrp.setItemText(8, _translate("MainWindow", "8"))
        self.comboBox_chnlgrp.setItemText(9, _translate("MainWindow", "9"))
        self.comboBox_chnlgrp.setItemText(10, _translate("MainWindow", "10"))
        self.comboBox_chnlgrp.setItemText(11, _translate("MainWindow", "11"))
        self.comboBox_chnlgrp.setItemText(12, _translate("MainWindow", "12"))
        self.comboBox_chnlgrp.setItemText(13, _translate("MainWindow", "13"))
        self.comboBox_chnlgrp.setItemText(14, _translate("MainWindow", "14"))
        self.comboBox_chnlgrp.setItemText(15, _translate("MainWindow", "15"))
        self.comboBox_chnlgrp.setItemText(16, _translate("MainWindow", "16"))
        self.comboBox_chnlgrp.setItemText(17, _translate("MainWindow", "17"))
        self.comboBox_chnlgrp.setItemText(18, _translate("MainWindow", "18"))
        self.comboBox_chnlgrp.setItemText(19, _translate("MainWindow", "19"))
        self.comboBox_chnlgrp.setItemText(20, _translate("MainWindow", "20"))
        self.comboBox_chnlgrp.setItemText(21, _translate("MainWindow", "21"))
        self.comboBox_chnlgrp.setItemText(22, _translate("MainWindow", "22"))
        self.comboBox_chnlgrp.setItemText(23, _translate("MainWindow", "23"))
        self.comboBox_chnlgrp.setItemText(24, _translate("MainWindow", "24"))
        self.comboBox_chnlgrp.setItemText(25, _translate("MainWindow", "25"))
        self.comboBox_chnlgrp.setItemText(26, _translate("MainWindow", "26"))
        self.comboBox_chnlgrp.setItemText(27, _translate("MainWindow", "27"))
        self.comboBox_chnlgrp.setItemText(28, _translate("MainWindow", "28"))
        self.comboBox_chnlgrp.setItemText(29, _translate("MainWindow", "29"))
        self.comboBox_chnlgrp.setItemText(30, _translate("MainWindow", "30"))
        self.comboBox_chnlgrp.setItemText(31, _translate("MainWindow", "31"))
        self.comboBox_chnlgrp.setItemText(32, _translate("MainWindow", "32"))
        self.label_11.setText(_translate("MainWindow", "信道:"))
        self.comboBox_chnl.setItemText(0, _translate("MainWindow", "0"))
        self.comboBox_chnl.setItemText(1, _translate("MainWindow", "1"))
        self.label_2.setText(_translate("MainWindow", "抄表间隔:"))
        self.label_3.setText(_translate("MainWindow", "秒"))
        self.label_4.setText(_translate("MainWindow", "重试次数:"))
        self.label_5.setText(_translate("MainWindow", "抄表报文:"))
        self.lineEdit_pkt645.setText(_translate("MainWindow", "68 80 24 59 01 00 14 68 11 04 33 32 34 33 C3 16"))
        self.label_12.setText(_translate("MainWindow", "抄表轮次:"))
        self.label_13.setText(_translate("MainWindow", "抄通率达到"))
        self.label_14.setText(_translate("MainWindow", "% 时停止"))
        self.pushButton_start.setText(_translate("MainWindow", "开始抄表"))
        self.pushButton_save.setText(_translate("MainWindow", "保存"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "户号"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "姓名"))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "表号"))
        self.treeWidget.headerItem().setText(3, _translate("MainWindow", "总电能"))
        self.treeWidget.headerItem().setText(4, _translate("MainWindow", "费率1电能"))
        self.treeWidget.headerItem().setText(5, _translate("MainWindow", "费率2电能"))
        self.treeWidget.headerItem().setText(6, _translate("MainWindow", "费率3电能"))
        self.treeWidget.headerItem().setText(7, _translate("MainWindow", "费率4电能"))
        self.treeWidget.headerItem().setText(8, _translate("MainWindow", "原始数据"))
        self.groupBox_2.setTitle(_translate("MainWindow", "状态"))
        self.progressBar.setFormat(_translate("MainWindow", "%v/%m"))
        self.label_15.setText(_translate("MainWindow", "轮次:"))
        self.label_curround.setText(_translate("MainWindow", "0"))
        self.label_17.setText(_translate("MainWindow", "抄通率:"))
        self.label_currate.setText(_translate("MainWindow", "0"))
        self.label_currate_2.setText(_translate("MainWindow", "%"))
        self.label_6.setText(_translate("MainWindow", "正在抄读:"))
        self.label_curmeter.setText(_translate("MainWindow", "------------"))
        self.label_8.setText(_translate("MainWindow", "次数:"))
        self.label_retry.setText(_translate("MainWindow", "0"))
        self.actionSaveAs.setText(_translate("MainWindow", "SaveAs"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionUpgBpSts.setText(_translate("MainWindow", "upgBpSts"))
        self.actionUpgTxm.setText(_translate("MainWindow", "upgTxm"))
        self.actionRdSnCfg.setText(_translate("MainWindow", "rdSnCfg"))
        self.actionUpgRdBack.setText(_translate("MainWindow", "upgRdBack"))
        self.actionRmParsed.setText(_translate("MainWindow", "rmParsed"))
        self.actionClear.setText(_translate("MainWindow", "clear"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

