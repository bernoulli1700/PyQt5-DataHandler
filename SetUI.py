from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from DefDataType import *

class SetUI(QWidget):
        
  def InitMenubar(self):
        self.menuBar = QMenuBar()
        self.fileMenu = self.menuBar.addMenu("&File")
        self.EditMenu = self.menuBar.addMenu("&Edit")
        self.ViewMenu = self.menuBar.addMenu("&View")

        File_OpenAction = QAction('Open',self)
        File_OpenAction.triggered.connect(self.FileOpenEvent)

        self.fileMenu.addAction("New")
        self.fileMenu.addAction(File_OpenAction)
        self.fileMenu.addAction("Save")


  def InitDirTreeView(self):
        root_path = "C:/Users/LGRnD/Desktop/PythonProj/230207-PyQt5Proj"
        self.model_file_system = QFileSystemModel()
        self.model_file_system.setRootPath(root_path)
        self.model_file_system.setReadOnly(False)
        self.DirTreeView = QTreeView()
        self.DirTreeView.setModel(self.model_file_system)
        self.DirTreeView.setRootIndex(self.model_file_system.index(root_path))
        self.DirTreeView.doubleClicked.connect(lambda index : self.item_double_clicked(index))
        self.DirTreeView.setDragEnabled(True)
  
  def InitDataTreeView(self):
      self.DataTreeModel = QStandardItemModel()
      self.DataTreeModel.appendRow(CellData())
      self.DataTreeModel.setHeaderData(0,Qt.Horizontal,"Cell Name")
      self.DataTreeModel.setHeaderData(1,Qt.Horizontal,"Data Tree")

      self.DataTreeView = QTreeView()
      self.DataTreeView.setModel(self.DataTreeModel)

      self.DataTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
      self.DataTreeView.customContextMenuRequested.connect(self.showContextMenu)

     


  def Plot(self):
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.grid()        

  def TableWidgetUI(self):
        #Table Define & Initialize
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(20):
            for j in range(4):
                self.tableWidget.setItem(i, j,QTableWidgetItem(str(0)))
  
  def ButtonUI(self):
      self.ClearPlotButton = QPushButton('Clear Plot',self)
      self.ClearPlotButton.clicked.connect(self.ClearPlotButtonEvent)
      self.LastIndex = None
      self.TableUpdateButton = QPushButton('Update',self)
      self.TableUpdateButton.clicked.connect(self.UpdateTableButtonEvent)
      
      #TableUpdateButton.clicked.connect()


  def SetLayout(self):
        #Layout Setting
        hbox1 = QHBoxLayout()
        hbox1_vbox1 = QVBoxLayout()
        hbox1_vbox1.addWidget(self.canvas)
        hbox1_vbox1.addWidget(NavigationToolbar(self.canvas, self))
        hbox_dummy = QHBoxLayout()
        hbox_dummy.addWidget(self.ClearPlotButton)
        hbox_dummy.addStretch()
        hbox_dummy.addStretch()
        hbox1_vbox1.addLayout(hbox_dummy)

        hbox1_vbox2 = QVBoxLayout()
        hbox1_vbox2.addWidget(self.tableWidget, stretch = 3)
        hbox1_vbox2.addWidget(self.TableUpdateButton)
        hbox1.addLayout(hbox1_vbox1, stretch = 3)
        hbox1.addLayout(hbox1_vbox2, stretch = 1)

        vbox_1 = QVBoxLayout()
        vbox_1.addWidget(self.DirTreeView)
        vbox_1.addWidget(self.DataTreeView)
        
        vbox_2 = QVBoxLayout()
        vbox_2.addLayout(hbox1)

        WorkingLayout = QHBoxLayout()
        WorkingLayout.addLayout(vbox_1,stretch = 1)
        WorkingLayout.addLayout(vbox_2,stretch = 3)

        PageLayout = QVBoxLayout()
        PageLayout.addWidget(self.menuBar)
        PageLayout.addLayout(WorkingLayout)

        self.setLayout(PageLayout)
        self.setWindowTitle('DataHandler')
        self.setGeometry(300, 100, 1000, 800)
        self.show()
