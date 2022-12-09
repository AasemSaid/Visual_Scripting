from PyQt5.QtCore import QSignalMapper
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from Nodeeditor.SystemProperties.HomeWindow import NodeEditorWindow
from Nodeeditor.SystemProperties.utils_no_qt import dumpException
from CalcSubWindow import CalculatorSubWindow
from Nodeeditor.SystemProperties.HomeWidget import *
import os
from Nodeeditor.SystemProperties.utils import loadStylesheets
import qss.nodeeditior_dark_resources

class CalculatorWindow(NodeEditorWindow):

    def initUI(self):
        self.name_company = 'Blenderfreak'
        self.name_product = 'Calculator NodeEditor'

        self.stylesheet_filename =  os.path.join(os.path.dirname(__file__), "qss/nodeeditor.qss")
        loadStylesheets(os.path.join(os.path.dirname(__file__), "qss/nodeeditor-dark.qss"),self.stylesheet_filename)


        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.createNodeDock()

        self.readSettings()

        self.setWindowTitle("Calculator Nodeeditor Example")

    def closeEvent(self, event):
        # event.accept()
        # return
        try:
            if self.maybeSave():
                event.accept()
            else:
                event.ignore()
        except Exception as e:
            dumpException(e)

    def updateMenus(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addAction(self.closeAllAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAct)
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)

        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.activeMdiChild())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def createActions(self):
        super().createActions()
        self.closeAct = QAction("Cl&ose", self, statusTip="Close the active window",
                                triggered=self.mdiArea.closeActiveSubWindow)

        self.closeAllAct = QAction("Close &All", self, statusTip="Close all the windows",
                                   triggered=self.mdiArea.closeAllSubWindows)

        self.tileAct = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)

        self.cascadeAct = QAction("&Cascade", self, statusTip="Cascade the windows",
                                  triggered=self.mdiArea.cascadeSubWindows)

        self.nextAct = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                               statusTip="Move the focus to the next window",
                               triggered=self.mdiArea.activateNextSubWindow)

        self.previousAct = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild,
                                   statusTip="Move the focus to the previous window",
                                   triggered=self.mdiArea.activatePreviousSubWindow)

        self.separatorAct = QAction(self)
        self.separatorAct.setSeparator(True)

        self.aboutAct = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)

    def onFileNew(self):
        try:
            subwnd=self.createMdiChild()
            subwnd.show()
        except Exception as e:dumpException(e)

    def about(self):
        QMessageBox.about(self, "About Calculator NodeEditor Example",
                          "The <b>Calculator NodeEditor</b> example demonstrates how to write multiple "
                          "document interface applications using PyQt5 and NodeEditor. For more information visit: "
                          "<a href='https://www.blenderfreak.com/'>www.BlenderFreak.com</a>")

    def createMenus(self):
        super().createMenus()
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateMenus()
        self.windowMenu.aboutToShow.connect(self.updateMenus)

    def createToolBars(self):
        pass

    def createNodeDock(self):
        self.listwidget = QListWidget()
        self.listwidget.addItem("Add")
        self.listwidget.addItem("Subtract")
        self.listwidget.addItem("Multiply")
        self.listwidget.addItem("Divide")

        self.items = QDockWidget("Node")
        self.items.setWidget(self.listwidget)
        self.items.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.items)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def readSettings(self):
        pass

    def createMdiChild(self):
        nodeeditor = CalculatorSubWindow()
        subwnd=self.mdiArea.addSubWindow(nodeeditor)
        return subwnd

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None
