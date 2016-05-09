# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'liveaudio.ui'
#
# Created: Wed Sep  2 11:15:42 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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
        LiveAudio.resize(765, 354)
        self.cancel_button = QtGui.QPushButton(LiveAudio)
        self.cancel_button.setGeometry(QtCore.QRect(660, 270, 99, 27))
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.start_recording_button = QtGui.QPushButton(LiveAudio)
        self.start_recording_button.setGeometry(QtCore.QRect(10, 270, 141, 27))
        self.start_recording_button.setObjectName(_fromUtf8("start_recording_button"))
        self.stop_recording_button = QtGui.QPushButton(LiveAudio)
        self.stop_recording_button.setGeometry(QtCore.QRect(150, 270, 141, 27))
        self.stop_recording_button.setObjectName(_fromUtf8("stop_recording_button"))
        self.spectrogram = QtGui.QGraphicsView(LiveAudio)
        self.spectrogram.setGeometry(QtCore.QRect(395, 20, 361, 211))
        self.spectrogram.setObjectName(_fromUtf8("spectrogram"))
        self.soundcard_idx = QtGui.QSpinBox(LiveAudio)
        self.soundcard_idx.setGeometry(QtCore.QRect(480, 270, 71, 27))
        self.soundcard_idx.setObjectName(_fromUtf8("soundcard_idx"))
        self.label = QtGui.QLabel(LiveAudio)
        self.label.setGeometry(QtCore.QRect(400, 270, 81, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.textBrowser = QtGui.QTextBrowser(LiveAudio)
        self.textBrowser.setGeometry(QtCore.QRect(10, 240, 521, 21))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.write_to_file = QtGui.QPushButton(LiveAudio)
        self.write_to_file.setGeometry(QtCore.QRect(290, 270, 101, 27))
        self.write_to_file.setObjectName(_fromUtf8("write_to_file"))
        self.threshold_spinBox = QtGui.QSpinBox(LiveAudio)
        self.threshold_spinBox.setGeometry(QtCore.QRect(480, 300, 71, 27))
        self.threshold_spinBox.setObjectName(_fromUtf8("threshold_spinBox"))
        self.threshold_label = QtGui.QLabel(LiveAudio)
        self.threshold_label.setGeometry(QtCore.QRect(400, 300, 71, 20))
        self.threshold_label.setObjectName(_fromUtf8("threshold_label"))
        self.graphicsView = QtGui.QGraphicsView(LiveAudio)
        self.graphicsView.setGeometry(QtCore.QRect(10, 20, 381, 211))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))

        self.retranslateUi(LiveAudio)
        QtCore.QMetaObject.connectSlotsByName(LiveAudio)

    def retranslateUi(self, LiveAudio):
        LiveAudio.setWindowTitle(_translate("LiveAudio", "LiveAudio", None))
        self.cancel_button.setText(_translate("LiveAudio", "Cancel", None))
        self.start_recording_button.setText(_translate("LiveAudio", "Start recording", None))
        self.stop_recording_button.setText(_translate("LiveAudio", "Stop recording", None))
        self.label.setText(_translate("LiveAudio", "Soundcard", None))
        self.write_to_file.setText(_translate("LiveAudio", "Write to file", None))
        self.threshold_label.setText(_translate("LiveAudio", "Threshold", None))

