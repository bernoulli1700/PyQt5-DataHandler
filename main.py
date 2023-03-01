from SetUI import *
from DefEvents import *

class MyApp(SetUI,DefEvents):
  def __init__(self):
      super().__init__()
      super().InitMenubar()
      super().InitDirTreeView()
      super().InitDataTreeView()
      super().Plot()
      super().TableWidgetUI()
      super().ButtonUI()
      super().SetLayout()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
