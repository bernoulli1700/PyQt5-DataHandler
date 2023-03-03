import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class Tab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.grid()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.setLayout(layout)

class MyTableWidget(QTableWidget):
    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Paste):
            clipboard = QApplication.clipboard()
            mimeData = clipboard.mimeData()
            if mimeData.hasFormat('application/vnd.ms-excel') or mimeData.hasFormat('text/plain'):
                # Get the text data from the clipboard
                text = clipboard.text()

                # Split the text into rows and columns
                rows = text.split('\n')
                rows.pop()
                if not rows:
                    return
                cols = rows[0].split('\t')
                RowNums = len(rows)
                ColNums = len(cols)

                # Get the selected cell
                selected = self.selectedIndexes()
                if len(selected) == 1:
                    row = selected[0].row()
                    col = selected[0].column()

                    # Resize the QTableWidget as needed
                    numRows = row + RowNums if row + RowNums > self.rowCount() else self.rowCount()
                    numCols = col + ColNums if col + ColNums > self.columnCount() else self.columnCount()
                    self.setRowCount(numRows)
                    self.setColumnCount(numCols)

                    # Paste the clipboard data across all cells
                    for i in range(RowNums):
                        for j in range(ColNums):
                            if row + i < self.rowCount() and col + j < self.columnCount() and j < len(rows[i].split('\t')):
                                item = QTableWidgetItem(rows[i].split('\t')[j])
                                self.setItem(row + i, col + j, item)

        else:
            super(MyTableWidget,self).keyPressEvent(event)