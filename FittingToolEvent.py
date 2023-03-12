from PyQt5.QtWidgets import *

class FittingToolClass(QWidget):
    def FittingToolEvent_Rev1(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Curve Fitting Tool')
        
        PageLayout = QHBoxLayout()
        RadioBoxButton = QVBoxLayout()
        groupbox = QGroupBox('Fit Curve Select')

        LinearCheck = QRadioButton('Linear')
        IrrationalCheck = QRadioButton('Irrational')
        RadioBoxButton.addWidget(LinearCheck)
        RadioBoxButton.addWidget(IrrationalCheck)
        RadioBoxButton.addStretch()
        RadioBoxButton.addStretch()
        groupbox.setLayout(RadioBoxButton)

        PageLayout.addWidget(groupbox)

        dialog.setLayout(PageLayout)
        dialog.setModal(True)
        dialog.setGeometry(200,200,1200,300)
        dialog.exec_()


        

    def FittingToolEvent_Rev0(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Curve Fitting Tool')

        ImportCellTable = QTableWidget(dialog)
        ImportCellTable.setEditTriggers(QTableWidget.NoEditTriggers)
        ImportCellTable.setColumnCount(1)
        ImportCellTable.setHorizontalHeaderLabels(['Name'])
        ImportCycleTable = QTableWidget(dialog)
        ImportCycleTable.setEditTriggers(QTableWidget.NoEditTriggers)
        ImportCycleTable.setColumnCount(1)
        ImportCycleTable.setHorizontalHeaderLabels(['Name'])

        ExportCellTable = QTableWidget(dialog)
        ExportCellTable.setEditTriggers(QTableWidget.NoEditTriggers)
        ExportCellTable.setColumnCount(1)
        ExportCellTable.setHorizontalHeaderLabels(['Name'])
        ExportCycleTable = QTableWidget(dialog)
        ExportCycleTable.setEditTriggers(QTableWidget.NoEditTriggers)
        ExportCycleTable.setColumnCount(1)
        ExportCycleTable.setHorizontalHeaderLabels(['Name'])

        #SettingPanelBox - hbox
        #ImportCellBox - vbox / ImportCycleBox - vbox / 
        SettingPanelBox = QHBoxLayout()
        ImportCellBox = QVBoxLayout()
        ImportCycleBox = QVBoxLayout()
        ExportCellBox = QVBoxLayout()
        ExportCycleBox = QVBoxLayout()

        for row in range(self.DataTreeModel.rowCount()):
            ImportCellDataItem = self.DataTreeModel.item(row)
            ImportCellTable.insertRow(row)
            ImportCellNameItem = QTableWidgetItem(ImportCellDataItem.text())
            ImportCellTable.setItem(row,0,ImportCellNameItem)
        
        for row in range(self.DataTreeModel.rowCount()):
            ExportCellDataItem = self.DataTreeModel.item(row)
            ExportCellTable.insertRow(row)
            ExportCellNameItem = QTableWidgetItem(ExportCellDataItem.text())
            ExportCellTable.setItem(row,0,ExportCellNameItem)
        
        def UpdateImportCycleTable(current):
            selected_index = current.row()
            selected_cell_data_item = self.DataTreeModel.item(selected_index)
            ImportCycleTable.setRowCount(0)
            for row in range(selected_cell_data_item.rowCount()):
                cycle_array_item = selected_cell_data_item.child(row)
                ImportCycleTable.insertRow(row)
                subitem_name_item = QTableWidgetItem(cycle_array_item.text())
                ImportCycleTable.setItem(row, 0, subitem_name_item)
                
        def UpdateExportCycleTable(current):
            selected_index = current.row()
            selected_cell_data_item = self.DataTreeModel.item(selected_index)
            ExportCycleTable.setRowCount(0)
            for row in range(selected_cell_data_item.rowCount()):
                cycle_array_item = selected_cell_data_item.child(row)
                ExportCycleTable.insertRow(row)
                subitem_name_item = QTableWidgetItem(cycle_array_item.text())
                ExportCycleTable.setItem(row, 0, subitem_name_item)

        ImportCellTable.selectionModel().currentRowChanged.connect(UpdateImportCycleTable)
        ExportCellTable.selectionModel().currentRowChanged.connect(UpdateExportCycleTable)

        ImportCellBox.addWidget(QLabel('Import Cell',self))
        ImportCellBox.addWidget(ImportCellTable)
        ImportCycleBox.addWidget(QLabel('Import Cycle',self))
        ImportCycleBox.addWidget(ImportCycleTable)
        ExportCellBox.addWidget(QLabel('Export Cell',self))
        ExportCellBox.addWidget(ExportCellTable)
        ExportCycleBox.addWidget(QLabel('Export Cycle',self))
        ExportCycleBox.addWidget(ExportCycleTable)

        #SettingPanelBox - hbox
        SettingPanelBox.addLayout(ImportCellBox, stretch=1)
        SettingPanelBox.addLayout(ImportCycleBox, stretch=1)
        SettingPanelBox.addLayout(ExportCellBox, stretch=1)
        SettingPanelBox.addLayout(ExportCycleBox, stretch=1)

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


        dialog.setLayout(PageLayout)
        dialog.setModal(True)
        dialog.setGeometry(200,200,1200,600)
        dialog.exec_()
