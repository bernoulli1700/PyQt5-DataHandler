from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QTreeView, QMenu, QAction, QMainWindow
from PyQt5.QtCore import Qt, QModelIndex

class TreeModel(QStandardItemModel):
    def __init__(self, parent=None):
        super(TreeModel, self).__init__(parent)
        self.setHorizontalHeaderLabels(["Tree item", "Subitem 1", "Subitem 2"])

        # Add some items to the model
        parent_item = self.invisibleRootItem()
        for i in range(3):
            item = QStandardItem(f"Item {i}")
            for j in range(2):
                subitem = QStandardItem(f"Subitem {j}")
                item.appendRow([subitem])
            parent_item.appendRow(item)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tree_view = QTreeView()
        self.setCentralWidget(self.tree_view)

        self.tree_model = TreeModel()
        self.tree_view.setModel(self.tree_model)

        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, point):
        index = self.tree_view.indexAt(point)
        if not index.isValid():
            return

        menu = QMenu(self)

        # Determine the depth of the item
        depth = 0
        parent_index = index.parent()
        while parent_index.isValid():
            parent_index = parent_index.parent()
            depth += 1

        # Add actions to the menu based on the depth of the item
        if depth == 0:
            action = QAction("Action 1", self)
            menu.addAction(action)
        elif depth == 1:
            action1 = QAction("Action 1", self)
            action2 = QAction("Action 2", self)
            menu.addAction(action1)
            menu.addAction(action2)
        elif depth == 2:
            action = QAction("Action 3", self)
            menu.addAction(action)

        menu.exec_(self.tree_view.mapToGlobal(point))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
