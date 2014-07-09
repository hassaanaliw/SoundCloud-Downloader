from PyQt4.QtCore import SIGNAL
import sys
from PyQt4 import QtCore, QtGui, uic
import SoundCloudDL

form_class = uic.loadUiType("gui.ui")[0]

class EmittingStream(QtCore.QObject):

    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.connect(self.dirbut, SIGNAL("clicked()"),self.dirbut_click)
        self.connect(self.dl,SIGNAL("clicked()"),self.dl_click)
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)


    def dirbut_click(self):
        file = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.dirline.setText(file)
    def dl_click(self):
        SoundCloudDL.main(self.url.text())

    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self, text):

        cursor = self.t.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.t.setTextCursor(cursor)
        self.t.ensureCursorVisible()



app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()