# -*- coding: utf-8 -*-
"""
A module containing ``NodeEditorWidget`` class
"""
import os

from PyQt5.QtWidgets import QWidget, QGraphicsItem, QVBoxLayout

from Calculator.CalculatorBaseNode import *
from Calculator.CalculatorBaseNode import CalculatorBaseNodeFunctions
from Calculator.InputNode import CalculatorNodeInputFunctions
from Nodeeditor.Node.NodeFunc import AllNodeFunctions
from Nodeeditor.SystemProperties.GraphicalView import DrawGraphicalView
from Nodeeditor.SystemProperties.SceneFunc import AllSceneFunctions, InvalidFile

from Calculator.OutputNode import CalculatorNodeOutputFunctions


class NodeEditorWidget(QWidget):
    Scene_class = AllSceneFunctions
    GraphicsView_class = DrawGraphicalView

    """The ``NodeEditorWidget`` class"""

    def __init__(self, parent: QWidget = None):
        """
        :param parent: parent widget
        :type parent: ``QWidget``

        :Instance Attributes:

        - **filename** - currently graph's filename or ``None``
        """
        super().__init__(parent)

        self.filename = None

        self.createHomeWidget()


    def createHomeWidget(self):
        """Set up this ``NodeEditorWidget`` with its layout,  :class:`~nodeeditor.node_scene.Scene` and
        :class:`~nodeeditor.node_graphics_view.QDMGraphicsView`"""
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # crate graphics scene
        self.scene = self.__class__.Scene_class()

        # create graphics view
        self.view = self.__class__.GraphicsView_class(self.scene.grScene, self)
        self.layout.addWidget(self.view)

    def isModified(self):
        return self.scene.isModified()

    def isFilenameSet(self) -> bool:
        """Do we have a graph loaded from file or are we creating a new one?

        :return: ``True`` if filename is set. ``False`` if it is a new graph not yet saved to a file
        :rtype: ''bool''
        """
        return self.filename is not None

    def getSelectedItems(self) -> list:
        """Shortcut returning `Scene`'s currently selected items

        :return: list of ``QGraphicsItems``
        :rtype: list[QGraphicsItem]
        """
        return self.scene.getSelectedItems()

    def hasSelectedItems(self) -> bool:
        """Is there something selected in the :class:`nodeeditor.node_scene.Scene`?

        :return: ``True`` if there is something selected in the `Scene`
        :rtype: ``bool``
        """
        return self.getSelectedItems() != []

    def canUndo(self) -> bool:
        """Can Undo be performed right now?

        :return: ``True`` if we can undo
        :rtype: ``bool``
        """
        return self.scene.history.canUndo()

    def canRedo(self) -> bool:
        """Can Redo be performed right now?

        :return: ``True`` if we can redo
        :rtype: ``bool``
        """
        return self.scene.history.canRedo()

    def getUserFriendlyFilename(self) -> str:
        """Get user friendly filename. Used in the window title

        :return: just a base name of the file or `'New Graph'`
        :rtype: ``str``
        """
        name = os.path.basename(self.filename) if self.isFilenameSet() else "New Graph"
        return name + ("*" if self.isModified() else "")

    def fileNew(self):
        self.scene.clear()
        self.filename = None
        self.scene.history.clear()
        self.scene.history.storeInitialHistoryStamp()


    def fileLoad(self, filename):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.scene.loadFromFile(filename)
            self.filename = filename

            # clear history
            self.scene.history.clear()
            self.scene.history.storeInitialHistoryStamp()

            return True
        except InvalidFile as e:
            print(e)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, "Error loading %s" % os.path.basename(filename), str(e))
            return False
        finally:
            QApplication.restoreOverrideCursor()

    def fileSave(self, filename=None):
        # when called with empty parameter, we won't store the filename
        if filename is not None: self.filename = filename
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.scene.saveToFile(self.filename)
        QApplication.restoreOverrideCursor()
        return True

    # def addNodes(self):
    #     """Testing method to create 3 `Nodes` with 3 `Edges` connecting them"""
    #     node1 = AllNodeFunctions(self.scene, "My Awesome Node 1", inputs=[0, 0, 0], outputs=[1, 5])
    #     node2 = AllNodeFunctions(self.scene, "My Awesome Node 2", inputs=[3, 3, 3], outputs=[1])
    #     node3 = AllNodeFunctions(self.scene, "My Awesome Node 3", inputs=[2, 2, 2], outputs=[1])
    #     node1.setPos(-350, -250)
    #     node2.setPos(-75, 0)
    #     node3.setPos(200, -200)
    #
    #     edge1 = AllEdgeFunctions(self.scene, node1.outputs[0], node2.inputs[0], edge_type=1)
    #     edge2 = AllEdgeFunctions(self.scene, node2.outputs[0], node3.inputs[0], edge_type=3)
    #     edge3 = AllEdgeFunctions(self.scene, node1.outputs[0], node3.inputs[2], edge_type=3)
    #
    #     # node = AllNodeFunctions(self.scene, "Node", inputs=[2, 2, 2], outputs=[1])
    #
    #
    #     self.scene.history.storeInitialHistoryStamp()


    def addCustomNode(self):
        """Testing method to create a custom Node with custom content"""

        class CustomNewNodeContent(QLabel):  # , Serializable):
            def __init__(self, node, parent=None):
                super().__init__("FooBar")
                self.node = node
                self.setParent(parent)

        class CustomNewAllNodeFunctions(AllNodeFunctions):
            NodeContent_class = CustomNewNodeContent

        self.scene.setNodeClassSelector(lambda data: CustomNewAllNodeFunctions)
        node = CustomNewAllNodeFunctions(self.scene, "A Custom Node 1", inputs=[0, 1, 2])

        print("node content:", node.content)

 # Functions to Draw node by press right click


    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        add = cmenu.addAction(" + add")
        sub = cmenu.addAction(" - sub")
        mult = cmenu.addAction(" ?? mult")
        div = cmenu.addAction(" ?? div")
        input = cmenu.addAction("Input")
        output = cmenu.addAction("Output")

        mouse_pos = event.pos()
        scene_pos = self.scene.grScene.views()[0].mapToScene(mouse_pos)

        action = cmenu.exec_(mouse_pos)

        if action == add:
            node = CalculatorBaseNodeFunctions(self.scene, op_code=0, op_title="Addition", inputs=[0, 1], outputs=[1])
            node.setPos(scene_pos.x(), scene_pos.y())
        elif action == sub:
            node = CalculatorBaseNodeFunctions(self.scene, op_code=0, op_title="Subtraction", inputs=[0, 1], outputs=[1])
            node.setPos(scene_pos.x(), scene_pos.y())
        elif action == mult:
            node = CalculatorBaseNodeFunctions(self.scene, op_code=0, op_title="Multiplication", inputs=[0, 1], outputs=[1])
            node.setPos(scene_pos.x(), scene_pos.y())
        elif action == div:
            node = CalculatorBaseNodeFunctions(self.scene, op_code=0, op_title="Division", inputs=[0, 1], outputs=[1])
            node.setPos(scene_pos.x(), scene_pos.y())
        elif action == input:
            node = CalculatorNodeInputFunctions(self.scene, inputs=[], outputs=[1])
            node.setPos(scene_pos.x(), scene_pos.y())
        elif action == output:

            node=CalculatorNodeOutputFunctions(self.scene,inputs=[0,1],outputs=[])
            node.setPos(scene_pos.x(), scene_pos.y())

            # node = CalculatorBaseNodeFunctions(self.scene, op_code=0, op_title="Output", inputs=[0, 1], outputs=[1])
            # node.setPos(scene_pos.x(), scene_pos.y())


# def addDebugContent(self):
    #     """Testing method to put random QGraphicsItems and elements into QGraphicsScene"""
    #     greenBrush = QBrush(Qt.green)
    #     outlinePen = QPen(Qt.black)
    #     outlinePen.setWidth(2)
    #
    #     rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
    #     rect.setFlag(QGraphicsItem.ItemIsMovable)
    #
    #     text = self.grScene.addText("This is my Awesome text!", QFont("Ubuntu"))
    #     text.setFlag(QGraphicsItem.ItemIsSelectable)
    #     text.setFlag(QGraphicsItem.ItemIsMovable)
    #     text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))
    #
    #
    #     widget1 = QPushButton("Hello World")
    #     proxy1 = self.grScene.addWidget(widget1)
    #     proxy1.setFlag(QGraphicsItem.ItemIsMovable)
    #     proxy1.setPos(0, 30)
    #
    #
    #     widget2 = QTextEdit()
    #     proxy2 = self.grScene.addWidget(widget2)
    #     proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
    #     proxy2.setPos(0, 60)
    #
    #
    #     line = self.grScene.addLine(-200, -200, 400, -100, outlinePen)
    #     line.setFlag(QGraphicsItem.ItemIsMovable)
    #     line.setFlag(QGraphicsItem.ItemIsSelectable)