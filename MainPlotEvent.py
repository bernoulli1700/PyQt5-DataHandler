from PyQt5.QtWidgets import *
from CustomWidgets import *

class MainPlotEvent(QWidget):
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
   