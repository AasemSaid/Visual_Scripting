import os
import sys
from PyQt5.QtWidgets import *

from CalcWindow import CalculatorWindow
# from Nodeeditor.SystemProperties.utils import loadStylesheet

sys.path.insert(0, os.path.join( os.path.dirname(__file__), "..", ".." ))

if __name__ == "__main__":
    app = QApplication(sys.argv)


    app.setStyle('Fusion')

    wnd = CalculatorWindow()
    wnd.show()


    sys.exit(app.exec_())
