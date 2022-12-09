from Nodeeditor.SystemProperties.HomeWidget import NodeEditorWidget
from PyQt5.QtCore import Qt
class CalculatorSubWindow(NodeEditorWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setTitle()

        self.scene.addHasBeenModifiedListener(self.setTitle())


    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())

