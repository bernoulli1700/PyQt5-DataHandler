import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem

class CycleArray(QStandardItem):
    UserRole = Qt.UserRole + 1

    def __init__(self, array = None):
        super().__init__()
        self.setText('EmtpyCycle')
        self.setEditable(True)
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

class CellData(QStandardItem):
    def __init__(self):
        super().__init__()
        self.setText('EmptyCell')
        self.setEditable(True)
        self.appendRow(CycleArray())
    
class FitCurveData(QStandardItem):
    UserRole_1 = Qt.UserRole + 1
    UserRole_2 = Qt.UserRole + 2
    
    def __init__(self):
        super().__init__()
        super().setText('EmptyFitCurve')
        self.setEditable(True)
        self.FitTypeIndex = 1
        self.FitDataPts = np.zeros((10,2))

    def data(self, role):
        if role == self.UserRole_1:
            return super().data(self.UserRole_1)
        elif role == self.UserRole_2:
            return super().data(self.UserRole_2)    
        else :
            return super().data(role)




