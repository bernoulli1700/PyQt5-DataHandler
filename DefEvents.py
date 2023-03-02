import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QModelIndex
from DefDataType import *
from CustomWidgets import *

class TreeViewEvent(QWidget):
    def showContextMenu(self,pos):
        index = self.DataTreeView.indexAt(pos)
        self.LastIndex = index
        if not index.isValid():
            depth = 0
        else :
            depth = 1

        # Determine the depth of the item
        parent_index = index.parent()
        while parent_index.isValid():
            parent_index = parent_index.parent()
            depth += 1

        menu = QMenu(self.DataTreeView)

        # Add actions to the menu based on the depth of the item
        if depth == 0:
            create_action = QAction('Create New', self)
            create_action.triggered.connect(self.CreateNewEvent)
            menu.addAction(create_action)
        elif depth == 1:
            delete_action = QAction('Delete Item', self)
            item = index.model().itemFromIndex(index)
            delete_action.triggered.connect(lambda: self.DeleteItemEvent(item))
            menu.addAction(delete_action)
        elif depth == 2:
            Plot_action = QAction('Plot', self)
            Edit_action = QAction('Edit', self)
            Plot_action.triggered.connect(lambda: self.TreeViewToPlotEvent(index))
            Edit_action.triggered.connect(lambda: self.TreeViewToEditEvent(index))
            menu.addAction(Plot_action)   
            menu.addAction(Edit_action)   

        menu.exec_(self.DataTreeView.viewport().mapToGlobal(pos))
    
    def CreateNewEvent(self):
        self.DataTreeModel.appendRow(CellData())
        self.DataTreeView.setModel(self.DataTreeModel)
    
    def DeleteItemEvent(self,item):
        # Remove the selected item from the model
        if item is not None :
            parent_item = item.parent()
            if parent_item is None:
                parent_item = self.DataTreeModel.invisibleRootItem()
            row = item.row()
            parent_item.takeRow(row)

            # Remove the selected item from the tree view
            selection_model = self.DataTreeView.selectionModel()
            selection_model.clearSelection()
            self.DataTreeView.setCurrentIndex(QModelIndex())
            self.DataTreeView.reset()

class PlotEvent(QWidget):
    def TreeViewToPlotEvent(self, index):
        item = index.model().itemFromIndex(index)
        array = item.data(item.UserRole)
        self.ax.plot(array[:,0],array[:,1], label = item.text())
        self.ax.legend()
        self.canvas.draw()

    def TreeViewToEditEvent(self, index):
        item = index.model().itemFromIndex(index)
        array = item.data(item.UserRole)

        #Update TableWidget
        RowNum = len(array[:,0])
        ColNum = len(array[0,:])

        PopUpTableWidget = MyTableWidget()
        PopUpTableWidget.setRowCount(RowNum)
        PopUpTableWidget.setColumnCount(ColNum)

        for row in range(0,RowNum):
            for col in range(0,ColNum):
                PopUpTableWidget.setItem(row,col,QTableWidgetItem(str(array[row,col])))
        
        dialog = QDialog(self)
        dialog.setWindowTitle('Edit Window')
        layout = QVBoxLayout()
        layout.addWidget(PopUpTableWidget)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        dialog.setModal(True)
        dialog.show()

        if dialog.exec_() == QDialog.Accepted:
            newarray = np.zeros([RowNum,ColNum])
            for n_row in range(0,RowNum):
                for n_col in range(0,ColNum):
                    newarray[n_row,n_col] = float(PopUpTableWidget.item(n_row,n_col).text())
            
            # Set the new edited values in the item
            item.setData(newarray,item.UserRole)

class ButtonEvent(QWidget):
    def ClearPlotButtonEvent(self):
        self.ax.clear()
        self.ax.grid()
        self.canvas.draw()

class MenuEvent(QWidget):
    pass

class DefEvents(PlotEvent, MenuEvent, ButtonEvent, TreeViewEvent):
    pass
