from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Nodeeditor.SystemProperties.utils_no_qt import dumpException
from CalculatorConfig import *


class GraphicalDragListBox(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.createListBox()

    def createListBox(self):
        #init
        self.setIconSize(QSize(32,32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.addNewItems()

    def addNewItems(self):
        self.addItem("Input", "icons/in.png",OP_NODE_INPUT)
        self.addItem("Output", "icons/out.png",OP_NODE_OUTPUT)
        self.addItem("Add", "icons/add.png", OP_NODE_ADD)
        self.addItem("Subtract", "icons/sub.png",OP_NODE_SUB)
        self.addItem("Multiply", "icons/mul.png", OP_NODE_MUL)
        self.addItem("Divide", "icons/divide.png", OP_NODE_DIV)

    def addItem(self, name,icon=None, op_code=0):
        item=QListWidgetItem(name, self)
        pixmap =QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(32,32))

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, op_code)

    def startDrag(self, *args, **kwargs):
        print("ListBox::startDrag")
        try:
            item=self.currentItem()
            op_code=item.data(Qt.UserRole +1)
            print("dragging item <%d>" % op_code, item)

            pixmap = QPixmap(item.data(Qt.UserRole))

            itemData = QByteArray()
            dataStream=QDataStream(itemData,QIODevice.WriteOnly)
            dataStream.writeInt(op_code)
            dataStream.writeQString(item.text())


            mimeData = QMimeData()
            mimeData.setData("application/x-item", itemData)

            drag=QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e: dumpException(e)

