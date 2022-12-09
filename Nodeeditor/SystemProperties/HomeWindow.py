# -*- coding: utf-8 -*-
"""
A module containing the Main Window class
"""
import json
import os

from PyQt5.QtCore import QSize, QSettings, QPoint
from PyQt5.QtWidgets import QMainWindow, QLabel, QAction, QMessageBox, QFileDialog, QApplication

from Nodeeditor.SystemProperties.HomeWidget import NodeEditorWidget
from Nodeeditor.SystemProperties.utils_no_qt import dumpException


class NodeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.name_company = 'Blenderfreak'
        self.name_product = 'NodeEditor'

        self.initUI()

    def createAct(self, name, shortcut, tooltip, callback):
        act = QAction(name, self)
        act.setShortcut(shortcut)
        act.setToolTip(tooltip)
        act.triggered.connect(callback)
        return act

    def initUI(self):

        self.createActions()
        self.createMenus()

        # create node editor widget
        self.nodeeditor = NodeEditorWidget(self)
        self.nodeeditor.scene.addHasBeenModifiedListener(self.setTitle)
        self.setCentralWidget(self.nodeeditor)

        # set window properties
        self.setGeometry(200, 200, 800, 600)
        self.setTitle()
        self.show()

    def createStatusBa(self):
        # status bar
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        self.nodeeditor.view.scenePosChanged.connect(self.onScenePosChanged)

    def createActions(self):
        self.actNew = QAction('&New', self, shortcut='Ctrl+N', statusTip="Create new graph", triggered=self.onFileNew)
        self.actOpen = QAction('&Open', self, shortcut='Ctrl+O', statusTip="Open file", triggered=self.onFileOpen)
        self.actSave = QAction('&Save', self, shortcut='Ctrl+S', statusTip="Save file", triggered=self.onFileSave)
        self.actSaveAs = QAction('Save &As...', self, shortcut='Ctrl+Shift+S', statusTip="Save file as...",
                                 triggered=self.onFileSaveAs)
        self.actExit = QAction('E&xit', self, shortcut='Ctrl+Q', statusTip="Exit application", triggered=self.close)

        self.actUndo = QAction('&Undo', self, shortcut='Ctrl+Z', statusTip="Undo last operation",
                               triggered=self.onEditUndo)
        self.actRedo = QAction('&Redo', self, shortcut='Ctrl+Shift+Z', statusTip="Redo last operation",
                               triggered=self.onEditRedo)
        self.actCut = QAction('Cu&t', self, shortcut='Ctrl+X', statusTip="Cut to clipboard", triggered=self.onEditCut)
        self.actCopy = QAction('&Copy', self, shortcut='Ctrl+C', statusTip="Copy to clipboard",
                               triggered=self.onEditCopy)
        self.actPaste = QAction('&Paste', self, shortcut='Ctrl+V', statusTip="Paste from clipboard",
                                triggered=self.onEditPaste)
        self.actDelete = QAction('&Delete', self, shortcut='Del', statusTip="Delete selected items",
                                 triggered=self.onEditDelete)
        self.actNew = self.createAct('&New', 'Ctrl+N', "Create new graph", self.onFileNew)
        self.actOpen = self.createAct('&Open', 'Ctrl+O', "Open file", self.onFileOpen)
        self.actSave = self.createAct('&Save', 'Ctrl+S', "Save file", self.onFileSave)
        self.actSaveAs = self.createAct('Save &As...', 'Ctrl+Shift+S', "Save file as...", self.onFileSaveAs)
        self.actExit = self.createAct('E&xit', 'Ctrl+Q', "Exit application", self.close)
        self.actUndo = self.createAct('&Undo', 'Ctrl+Z', "Undo last operation", self.onEditUndo)
        self.actRedo = self.createAct('&Redo', 'Ctrl+Shift+Z', "Redo last operation", self.onEditRedo)
        self.actCut = self.createAct('Cu&t', 'Ctrl+X', "Cut to clipboard", self.onEditCut)
        self.actCopy = self.createAct('&Copy', 'Ctrl+C', "Copy to clipboard", self.onEditCopy)
        self.actPaste = self.createAct('&Paste', 'Ctrl+V', "Paste from clipboard", self.onEditPaste)
        self.actDelete = self.createAct('&Delete', 'Del', "Delete selected items", self.onEditDelete)

    def createMenus(self):
        menubar = self.menuBar()

        # initialize Menu
        self.fileMenu = menubar.addMenu('&File')
        self.fileMenu.addAction(self.actNew)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actOpen)
        self.fileMenu.addAction(self.actSave)
        self.fileMenu.addAction(self.actSaveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actExit)

        self.editMenu = menubar.addMenu('&Edit')
        self.editMenu.addAction(self.actUndo)
        self.editMenu.addAction(self.actRedo)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actCut)
        self.editMenu.addAction(self.actCopy)
        self.editMenu.addAction(self.actPaste)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actDelete)

    def setTitle(self):
        title = "Node Editor - "
        title += self.getCurrentNodeWidget().getUserFriendlyFilename()

        self.setWindowTitle(title)

    def closeEvent(self, event):
        try:
            if self.maybeSave():
                event.accept()
            else:
                event.ignore()
        except Exception as e:
            dumpException(e)

    # def isModified(self):
    #     return self.getCurrentNodeWidget().scene.has_been_modified

    def getCurrentNodeWidget(self):
        return self.centralWidget()

    def maybeSave(self):
        # if not self.isModified():
        #     return True
        #
        res = QMessageBox.warning(self, "About to loose your work?",
                                  "The document has been modified.\n Do you want to save your changes?",
                                  QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
                                  )

        if res == QMessageBox.Save:
            return self.onFileSave()
        elif res == QMessageBox.Cancel:
            return False

        return True

    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    def onFileNew(self):
        if self.maybeSave():
            self.getCurrentNodeWidget().scene.clear()
            self.filename = None
            self.setTitle()

    def onFileOpen(self):
        if self.maybeSave():
            fname, filter = QFileDialog.getOpenFileName(self, 'Open graph from file')
            if fname == '':
                return
            if os.path.isfile(fname):
                self.getCurrentNodeWidget().scene.loadFromFile(fname)
                self.filename = fname
                self.setTitle()

    def onFileSave(self):
        if self.filename is None: return self.onFileSaveAs()
        self.getCurrentNodeWidget().scene.saveToFile(self.filename)
        self.statusBar().showMessage("Successfully saved %s" % self.filename)
        return True

    def onFileSaveAs(self):
        fname, filter = QFileDialog.getSaveFileName(self, 'Save graph to file')
        if fname == '':
            return False
        self.filename = fname
        self.onFileSave()
        return True

    def onEditUndo(self):
        self.getCurrentNodeWidget().scene.history.undo()

    def onEditRedo(self):
        self.getCurrentNodeWidget().scene.history.redo()

    def onEditDelete(self):
        self.getCurrentNodeWidget().scene.grScene.views()[0].deleteSelected()

    def onEditCut(self):
        data = self.getCurrentNodeWidget().scene.clipboard.serializeSelected(delete=True)
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        data = self.getCurrentNodeWidget().scene.clipboard.serializeSelected(delete=False)
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        raw_data = QApplication.instance().clipboard().text()

        try:
            data = json.loads(raw_data)
        except ValueError as e:
            print("Pasting of not valid json data!", e)
            return

        # check if the json data are correct
        if 'nodes' not in data:
            print("JSON does not contain any nodes!")
            return

        self.centralWidget().scene.clipboard.deserializeFromClipboard(data)

    def readSettings(self):
        settings = QSettings(self.name_company, self.name_product)
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QSettings(self.name_company, self.name_product)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())
