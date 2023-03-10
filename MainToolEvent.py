from PyQt5.QtWidgets import *
from FittingToolEvent import *
from PointHandlerEvent import *

class MainToolClass(FittingToolClass,PointHandlerClass):
    def ClearPlotEvent(self):
        current_tab = self.tabs.currentWidget()
        current_tab.ax.clear()
        current_tab.ax.grid()
        current_tab.canvas.draw()

