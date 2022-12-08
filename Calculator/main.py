import sys
from PyQt5.QtWidgets import *

from CalcWindow import CalculatorWindow

if __name__ =="__main__":
    app=QApplication(sys.argv)

    wnd=CalculatorWindow()
    wnd.show()
    sys.exit(app.exec_())

