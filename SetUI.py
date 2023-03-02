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

        self.fileMenu.addAction("New")
        self.fileMenu.addAction(File_OpenAction)
        self.fileMenu.addAction("Save")


  def InitDirTreeView(self):
        root_path = "C:/Users/LGRnD/Desktop/PythonProj/PyQt5-DataHandler"
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

  def ButtonUI(self):
      self.ClearPlotButton = QPushButton('Clear Plot',self)
      self.ClearPlotButton.clicked.connect(self.ClearPlotButtonEvent)
      self.LastIndex = None

  def SetLayout(self):
        #Layout Setting

        #PageLayout - vbox
        #self.menubar / WorkingLayout - hbox

        #WorkingLayout - hbox
        #WorkingLayout_Left - vbox / WorkingLayout_Right - vbox

        #WorkingLayout_Left - vbox
        #self.DirTreeView / self.DataTreeView

        #WorkingLayout_Right - vbox
        #self.canvas / NavigationToobar / ButtonToolBox - hbox

        #BottonToolBox - hbox
        #self.ClearPlotButton / Stretch / Stretch

        WorkingLayout_Left = QVBoxLayout()
        WorkingLayout_Left.addWidget(self.DirTreeView)
        WorkingLayout_Left.addWidget(self.DataTreeView)
        
        ButtonToolBox = QHBoxLayout()
        ButtonToolBox.addWidget(self.ClearPlotButton)
        ButtonToolBox.addStretch()
        ButtonToolBox.addStretch()
        
        WorkingLayout_Right = QVBoxLayout()
        WorkingLayout_Right.addWidget(self.canvas)
        WorkingLayout_Right.addWidget(NavigationToolbar(self.canvas,self))
        WorkingLayout_Right.addLayout(ButtonToolBox)
     
        WorkingLayout = QHBoxLayout()
        WorkingLayout.addLayout(WorkingLayout_Left,stretch = 1)
        WorkingLayout.addLayout(WorkingLayout_Right,stretch = 3)

        PageLayout = QVBoxLayout()
        PageLayout.addWidget(self.menuBar)
        PageLayout.addLayout(WorkingLayout)

        self.setLayout(PageLayout)
        self.setWindowTitle('DataHandler')
        self.setGeometry(300, 100, 1000, 800)
        self.show()
