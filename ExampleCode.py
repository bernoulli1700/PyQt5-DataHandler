import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt

class CycleArray(QStandardItem):
    UserRole = Qt.UserRole + 1

    def __init__(self, array=None):
        super().__init__()
        self.setText('EmptyCycle')
        self.setEditable(True)
        if array is None:
            array = np.zeros([40, 2])
            array[:, 0] = np.arange(1, 41, 1)
            array[:, 1] = np.arange(1, 41, 1)
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tree_view = QTreeView()
        self.model = QStandardItemModel()
        self.tree_view.setModel(self.model)

        root_item = self.model.invisibleRootItem()
        for i in range(5):
            cell_data_item = CellData()
            cell_data_item.setText(f'Cell Data {i}')
            root_item.appendRow(cell_data_item)

        self.setCentralWidget(self.tree_view)

        self.fit_tool_button = QPushButton('Fitting Tool', self)
        self.fit_tool_button.clicked.connect(self.open_fitting_dialog)
        self.tool_bar = self.addToolBar('Fit Tool')
        self.tool_bar.addWidget(self.fit_tool_button)

    def open_fitting_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Fitting Tool')

        cell_table = QTableWidget(dialog)
        cell_table.setColumnCount(2)
        cell_table.setHorizontalHeaderLabels(['Name', 'Value'])
        for row in range(self.model.rowCount()):
            cell_data_item = self.model.item(row)
            cell_table.insertRow(row)
            cell_name_item = QTableWidgetItem(cell_data_item.text())
            cell_table.setItem(row, 0, cell_name_item)

        subitem_table = QTableWidget(dialog)
        subitem_table.setColumnCount(2)
        subitem_table.setHorizontalHeaderLabels(['Name', 'Value'])

        def update_subitem_table(current, previous):
            selected_index = current.row()
            selected_cell_data_item = self.model.item(selected_index)
            subitem_table.setRowCount(0)
            for row in range(selected_cell_data_item.rowCount()):
                cycle_array_item = selected_cell_data_item.child(row)
                subitem_table.insertRow(row)
                subitem_name_item = QTableWidgetItem(f'Cycle Array {row}')
                subitem_table.setItem(row, 0, subitem_name_item)
                subitem_value_item = QTableWidgetItem(str(cycle_array_item.array))
                subitem_table.setItem(row, 1, subitem_value_item)

        cell_table.selectionModel().currentRowChanged.connect(update_subitem_table)

        ok_button = QPushButton('OK')
        cancel_button = QPushButton('Cancel')
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout = QVBoxLayout()
        layout.addWidget(cell_table)
        layout.addWidget(subitem_table)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)
        dialog.exec_()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
