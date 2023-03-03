import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QModelIndex
from DefDataType import *
from CustomWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

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
            create_action = QAction('Create New Cell Data', self)
            create_action.triggered.connect(self.CreateNewCellDataEvent)
            menu.addAction(create_action)
        elif depth == 1:
            item = index.model().itemFromIndex(index)
            Create_action = QAction('Create New Cycle Array', self)
            delete_action = QAction('Delete', self)
            delete_action.triggered.connect(lambda: self.DeleteDataEvent(item))
            Create_action.triggered.connect(lambda: self.CreateNewCycleEvent(item))
            menu.addAction(Create_action)   
            menu.addAction(delete_action)
        elif depth == 2:
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
        self.DataTreeModel.appendRow(CellData())
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


class PlotEvent(QWidget):
    def TreeViewPlotEvent(self, item):
        array = item.data(item.UserRole)
        current_tab = self.tabs.currentWidget()
        current_tab.ax.plot(array[:,0],array[:,1], label = item.text())
        current_tab.ax.legend()
        current_tab.canvas.draw()
    
    def add_tab(self):
        tab = Tab()
        tab_name = "Tab {}".format(self.tabs.count() + 1)
        tab.canvas.setContextMenuPolicy(Qt.CustomContextMenu)
        tab.canvas.customContextMenuRequested.connect(self.show_context_menu)
        self.tabs.addTab(tab, tab_name)
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
        

    def close_tab(self, index):
        self.tabs.removeTab(index)

    def rename_tab(self, index):
        tab_name, ok = QInputDialog.getText(self, "Rename tab", "New tab name:",
                                            QLineEdit.Normal, self.tabs.tabText(index))
        if ok:
            self.tabs.setTabText(index, tab_name)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        new_plot_action = menu.addAction("Create new plot")
        action = menu.exec_(self.tabs.currentWidget().mapToGlobal(pos))
        if action == new_plot_action:
            self.add_tab()

    def rename_tab(self, index):
        tab_name, ok = QInputDialog.getText(self, "Rename tab", "New tab name:",
                                            QLineEdit.Normal, self.tabs.tabText(index))
        if ok:
            self.tabs.setTabText(index, tab_name)
   
class ButtonEvent(QWidget):
    def ClearPlotButtonEvent(self):
        current_tab = self.tabs.currentWidget()
        current_tab.ax.clear()
        current_tab.ax.grid()
        current_tab.canvas.draw()

    def FittingToolButtonEvent(self):

        ImportCellDataSelectonTable = QTableWidget()
        ImportCellDataSelectonTable.setRowCount(4)
        ImportCellDataSelectonTable.setColumnCount(1)
        ImportCycleDataSelectonTable = QTableWidget()
        ImportCycleDataSelectonTable.setRowCount(4)
        ImportCycleDataSelectonTable.setColumnCount(1)

        ExportCellDataSelectonTable = QTableWidget()
        ExportCellDataSelectonTable.setRowCount(4)
        ExportCellDataSelectonTable.setColumnCount(1)
        ExportCycleDataSelectonTable = QTableWidget()
        ExportCycleDataSelectonTable.setRowCount(4)
        ExportCycleDataSelectonTable.setColumnCount(1)

        #SettingPanelBox - hbox
        #ImportCellDataSelectionBox - vbox / ImportCycleDataSelectionBox - vbox / 
        SettingPanelBox = QHBoxLayout()
        ImportCellDataSelectionBox = QVBoxLayout()
        ImportCycleDataSelectionBox = QVBoxLayout()
        ExportCellDataSelectionBox = QVBoxLayout()
        ExportCycleDataSelectionBox = QVBoxLayout()

        ImportCellDataSelectionBox.addWidget(ImportCellDataSelectonTable)
        ImportCycleDataSelectionBox.addWidget(ImportCycleDataSelectonTable)
        ExportCellDataSelectionBox.addWidget(ExportCellDataSelectonTable)
        ExportCycleDataSelectionBox.addWidget(ExportCycleDataSelectonTable)

        #SettingPanelBox - hbox
        SettingPanelBox.addLayout(ImportCellDataSelectionBox, stretch=1)
        SettingPanelBox.addLayout(ImportCycleDataSelectionBox, stretch=1)
        SettingPanelBox.addLayout(ExportCellDataSelectionBox, stretch=1)
        SettingPanelBox.addLayout(ExportCycleDataSelectionBox, stretch=1)

        #ControlPanelBox - hbox
        #FittingCurveSwitchBox - vbox / FittingParameterBox - vbox
        ControlPanelBox = QHBoxLayout()
        FittingCurveSwitchBox = QVBoxLayout()
        FittingCurveSwitchBox.addStretch()
        FittingParameterBox = QVBoxLayout()
        FittingParameterBox.addStretch()
        ControlPanelBox.addLayout(FittingCurveSwitchBox,stretch=1)
        ControlPanelBox.addLayout(FittingParameterBox,stretch=3)
        

        #PageLayout - vbox
        #SettingPanelBox - hbox / ControlPanelBox - hbox 
        PageLayout = QVBoxLayout()
        PageLayout.addLayout(SettingPanelBox, stretch=1)
        PageLayout.addLayout(ControlPanelBox, stretch=1)


        dialog = QDialog(self)
        dialog.setWindowTitle('Curve Fitting Tool')
        dialog.setLayout(PageLayout)
        dialog.setModal(True)
        dialog.setGeometry(200,200,1200,600)
        dialog.show()


class MenuEvent(QWidget):
    pass

class DefEvents(PlotEvent, MenuEvent, ButtonEvent, TreeViewEvent):
    pass
