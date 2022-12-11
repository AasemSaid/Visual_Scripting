from PyQt5.QtGui import *

from Nodeeditor.SystemProperties.HomeWidget import NodeEditorWidget
from PyQt5.QtCore import *
from CalculatorConfig import *


class CalculatorSubWindow(NodeEditorWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setTitle()

        self.scene.addHasBeenModifiedListener(self.setTitle)
        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)

        self._close_event_listeners = []

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)

    def onDragEnter(self, event):
        print("CalcSubWnd :: ~onDragEnter")
        print("text: '%s'" % event.mimeData().text())
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            # print("..... denied drag enter event")
            event.setAccepted(False)

    def onDrop(self, event):
        # print("CalcSubWnd :: ~onDrop")
        # print("text: '%s'" % event.mimeData().text())
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            op_code = dataStream.readInt()
            text = dataStream.readQString()

            print("GOT DROP: [%d] '%s'" % (op_code, text))
            # print("dragging item <%d>" % op_code)


            # mouse_position = event.pos()
            # scene_position = self.scene.views()[0].mapToScene(mouse_position)

            event.setDropAction(Qt.MoveAction)
            event.accept()

        else:
            # print(" ... drop ignored, not requested format '%s'" % LISTBOX_MIMETYPE)
            event.ignore()

