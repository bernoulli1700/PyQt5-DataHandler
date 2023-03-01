import sys
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel

class FCycleArray(QStandardItem):
    UserRole = Qt.UserRole + 1

    def __init__(self, array = None):
        super().__init__()
        self.setText('FCycle')
        self.setEditable(False)
        if array is None:
            array = np.zeros([40,2])
            array[:,0] = np.arange(1,41,1)
            array[:,1] = np.arange(1,41,1)
        self.array = array
        self.setData(self.array, self.UserRole)

    def data(self, role):
        if role == self.UserRole:
            return super().data(self.UserRole)
        else:
            return super().data(role)

class DCycleArray(QStandardItem):
    UserRole = Qt.UserRole + 1

    def __init__(self, array = None):
        super().__init__()
        self.setText('DCycle')
        self.setEditable(False)
        if array is None:
            array = np.zeros([40,2])
            array[:,0] = np.arange(1,41,1)
            array[:,1] = np.arange(0.5,20.5,0.5)
        self.array = array
        self.setData(self.array, self.UserRole)

    def data(self, role):
        if role == self.UserRole:
            return super().data(self.UserRole)
        else:
            return super().data(role)

class CellData(QStandardItem):
    def __init__(self):
        super().__init__()
        self.setText('EmptyCell')
        self.setEditable(True)
        self.appendRow(FCycleArray())
        self.appendRow(DCycleArray())

