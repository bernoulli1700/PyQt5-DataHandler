from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from MainTreeViewEvent import *
from MainPlotEvent import *
from MainToolEvent import *



class MenuEvent(QWidget):
    pass

class DefEvents(MainTreeViewEvent, MainPlotEvent, MenuEvent, MainToolClass):
    pass
