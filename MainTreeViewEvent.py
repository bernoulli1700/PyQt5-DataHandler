from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import *
from DefDataType import *
from CustomWidgets import *

class MainTreeViewEvent(QWidget):
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
        item = self.DataTreeModel.itemFromIndex(index)
        # Add actions to the menu based on the depth of the item
        if depth == 1:
            if isinstance(item, CellData):
                create_action = QAction('Create New Cell Data', self)
                create_action.triggered.connect(self.CreateNewCellDataEvent)
                menu.addAction(create_action)
            if isinstance(item, FitCurveData):
                create_action = QAction('Create New Fit Curve Data', self)
                create_action.triggered.connect(self.CreateNewFitCurveDataEvent)
                menu.addAction(create_action)
        elif depth == 2:
            if isinstance(item, CellData):
                item = index.model().itemFromIndex(index)
                Create_action = QAction('Create New Cycle Array', self)
                delete_action = QAction('Delete', self)
                delete_action.triggered.connect(lambda: self.DeleteDataEvent(item))
                Create_action.triggered.connect(lambda: self.CreateNewCycleEvent(item))
                menu.addAction(Create_action)   
                menu.addAction(delete_action)
        elif depth == 3:
            if isinstance(item, CycleArray):
                item = index.model().itemFromIndex(index)
                Delete_action = QAction('Delete', self)
                Plot_action = QAction('Plot', self)
                Edit_action = QAction('Edit', self)
                Plot_action.triggered.connect(lambda: self.TreeViewPlotEvent(item))
                Delete_action.triggered.connect(lambda: self.DeleteDataEvent(item))
                Edit_action.triggered.connect(lambda: self.CycleEditEvent(item))
                menu.addAction(Delete_action)   
                menu.addAction(Plot_action)   
                menu.addAction(Edit_action)   

        menu.exec_(self.DataTreeView.viewport().mapToGlobal(pos))
    
    def CreateNewCellDataEvent(self):
        self.CellDataTree.appendRow(CellData())
        self.DataTreeView.setModel(self.DataTreeModel)

    def CreateNewFitCurveDataEvent(self):
        self.FitCurveDataTree.appendRow(FitCurveData())
        self.DataTreeView.setModel(self.DataTreeModel)

    def CreateNewCycleEvent(self, item):
        item.appendRow(CycleArray())
        self.DataTreeView.setModel(self.DataTreeModel)

    def DeleteDataEvent(self,item):
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

    def CycleEditEvent(self, item):
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
