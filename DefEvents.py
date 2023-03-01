import csv
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QModelIndex
from DefDataType import *

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
            plot_action = QAction('Plot', self)
            plot_action.triggered.connect(lambda: self.TreeViewToPlotEvent(index))
            menu.addAction(plot_action)   

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

        #Update TableWidget
        RowNum = len(array[:,0])
        ColNum = len(array[0,:])
        self.tableWidget.setRowCount(RowNum)
        self.tableWidget.setColumnCount(ColNum)

        for i in range(0,RowNum):
            for j in range(0,ColNum):
                self.tableWidget.setItem(i, j,QTableWidgetItem(str(array[i,j])))



class TableEvent(QWidget):
  def UpdateTableWidget(self):
        FileHandle = open(self.ImportFile_QLine.text(),'r',encoding='utf-8')
        ReadLines = csv.reader(FileHandle)
        self.TableData = []
        for ReadLine in ReadLines:
            if ReadLine[0] == 'X':
                continue
            self.TableData.append([float(ReadLine[0]),float(ReadLine[1])])    
        self.TableData = np.array(self.TableData)
        self.tableWidget.setRowCount(len(self.TableData))
        self.tableWidget.setColumnCount(len(self.TableData[0]))

        for n_row in range(0,len(self.TableData)):
            for n_col in range(0,len(self.TableData[0])):
                self.tableWidget.setItem(n_row,n_col,QTableWidgetItem(str(self.TableData[n_row,n_col])))
    
  def SaveTableWidget(self):
        conditionA = self.ExportFile_Name != ''
        conditionB = self.ExportFile_QLine.text() != ''
        if conditionA and conditionB:
            FileName = str(self.ExportFile_QLine.text()) + '/' + self.ExportFile_Name.text()
            FileHandle = open(FileName,'w',encoding='utf-8',newline='')
            CsvWriter = csv.writer(FileHandle)
            for n_row in range(0,self.tableWidget.rowCount()):
                rowdata = []
                for n_col in range(0,self.tableWidget.columnCount()):
                    rowdata.append(self.tableWidget.item(n_row,n_col).text())
                CsvWriter.writerow(rowdata)
            FileHandle.close()

class ButtonEvent(QWidget):
    def ClearPlotButtonEvent(self):
        self.ax.clear()
        self.ax.grid()
        self.canvas.draw()

    def UpdateTableButtonEvent(self):
        if self.LastIndex == None:
            return
        item = self.LastIndex.model().itemFromIndex(self.LastIndex)
        RowNum = self.tableWidget.rowCount();
        ColNum = self.tableWidget.columnCount();
        newarray = np.zeros([RowNum,ColNum])
        for n_row in range(0,RowNum):
            for n_col in range(0,ColNum):
                newarray[n_row,n_col] = float(self.tableWidget.item(n_row,n_col).text())
        item.setData(newarray,item.UserRole)
        self.ax.plot(newarray[:,0],newarray[:,1], label = item.text())
        self.ax.legend()
        self.canvas.draw()
     

class MenuEvent(QWidget):
  def FileOpenEvent(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname[0] != '':
            f = open(fname[0], 'r')
            FileHandle = open(fname[0],'r',encoding='utf-8')
            ReadLines = csv.reader(FileHandle)
            self.TableData = []
            for ReadLine in ReadLines:
                if ReadLine[0] == 'X':
                    continue
                self.TableData.append([float(ReadLine[0]),float(ReadLine[1])])    
            self.TableData = np.array(self.TableData)
            self.tableWidget.setRowCount(len(self.TableData))
            self.tableWidget.setColumnCount(len(self.TableData[0]))

            for n_row in range(0,len(self.TableData)):
                for n_col in range(0,len(self.TableData[0])):
                    self.tableWidget.setItem(n_row,n_col,QTableWidgetItem(str(self.TableData[n_row,n_col])))
            f.close()
            self.ax.clear()
            self.UpdateTableData()
            self.ax.plot(self.TableData[:,0],self.TableData[:,1])
            self.ax.grid()
            self.canvas.draw()

  def showDialog2(self):
        fname = QFileDialog.getExistingDirectory(self, 'Open file', './')
        if fname != '':
            self.ExportFile_QLine.setText(fname)

class Subroutine(QWidget):
    def UpdateTableData(self):
        for n_row in range(0,self.tableWidget.rowCount()):
            for n_col in range(0,self.tableWidget.columnCount()):
                self.TableData[n_row,n_col] = float(self.tableWidget.item(n_row,n_col).text())

class DefEvents(PlotEvent, TableEvent, MenuEvent, ButtonEvent, Subroutine, TreeViewEvent):
    pass
