# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'liveaudio.ui'
#
# Created: Mon Aug 24 18:38:27 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import pyqtgraph as pg

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_LiveAudio(object):
    def setupUi(self, LiveAudio):
        LiveAudio.setObjectName(_fromUtf8("LiveAudio"))
        LiveAudio.resize(400, 300)
        self.verticalLayoutWidget = QtGui.QWidget(LiveAudio)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 19, 381, 211))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        #self.graphicsView = QtGui.QGraphicsView(self.verticalLayoutWidget)

        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.verticalLayout.addWidget(self.graphicsView)
        self.pushButton = QtGui.QPushButton(LiveAudio)
        self.pushButton.setGeometry(QtCore.QRect(290, 240, 99, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(LiveAudio)
        self.pushButton_2.setGeometry(QtCore.QRect(190, 240, 99, 27))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.retranslateUi(LiveAudio)
        QtCore.QMetaObject.connectSlotsByName(LiveAudio)

    def retranslateUi(self, LiveAudio):
        LiveAudio.setWindowTitle(_translate("LiveAudio", "LiveAudio", None))
        self.pushButton.setText(_translate("LiveAudio", "OK", None))
        self.pushButton_2.setText(_translate("LiveAudio", "Cancel", None))

