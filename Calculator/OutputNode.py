from PyQt5.QtGui import QImage, QColor, QPen, QBrush
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from Nodeeditor.Node.NodeFunc import AllNodeFunctions
from Nodeeditor.Socket.SocketFunc import LEFT_CENTER, RIGHT_CENTER
from Nodeeditor.SystemProperties.HomeWidget import *
from Nodeeditor.Node.GraphicalNode import *
from Nodeeditor.Node.ContentWidgetFunc import AllContentWidgetFunctions
from Nodeeditor.Node.GraphicalNode import DrawGraphicalNode
from Nodeeditor.SystemProperties.utils_no_qt import dumpException


class CalculatorOutputGraphicalNode(DrawGraphicalNode):
    def initSizes(self):
        """Set up internal attributes like `width`, `height`, etc."""
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_roundness = 6
        self.edge_padding = 8
        # self.title_horizontal_padding = 8
        # self.title_vertical_padding = 10

        # dh 3shan t8yr l font wl color bto3 l node l gdeda
        # def classAssets(self):
        # """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        # self.title_color = QColor("#FFFFFF")
        # self.title_font = QFont("Cairo", 10)

        self.color_default = QColor("#ef974d")
        self.pen_default = QPen(self.color_default)
        self.pen_default.setWidthF(2.0)

        self.color_selected = QColor("#F87217")
        self.pen_selected = QPen(self.color_selected)
        self.pen_selected.setWidthF(2.0)

        self.color_hovered = QColor("#F87217")
        self.pen_hovered = QPen(self.color_hovered)
        self.pen_hovered.setWidthF(3.0)

        self.brush_title = QBrush(QColor("#131922"))
        self.brush_background = QBrush(QColor("#1A202C"))


class CalcOutputContent(AllContentWidgetFunctions):
    def createContentWidget(self):
        self.edit = QLineEdit("50", self)
        self.edit.setAlignment(Qt.AlignCenter)
        self.edit.setStyleSheet("color: Red;"
                                "background-color:Orange;")

        # self.edit.setObjectName(self.node.content_label_objname)

    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


class CalculatorNodeOutputFunctions(AllNodeFunctions):
    GraphicsNode_class = CalculatorOutputGraphicalNode
    NodeContent_class = CalcOutputContent

    def __init__(self, scene, inputs=[], outputs=[]):
        self.op_title = "OUTPUT NODE"
        # self.content_label = content_label
        # content_label = "", content_label_objname = "calc_node_bg",
        # self.content_label_objname = content_label_objname

        super().__init__(scene, self.op_title, inputs, outputs)

    def getInnerClasses(self):
        node_content_class = self.getNodeContentClass()
        graphics_node_class = self.getGraphicsNodeClass()
        if node_content_class is not None: self.content = node_content_class(self)
        if graphics_node_class is not None: self.grNode = graphics_node_class(self)

    def getNodeContentClass(self):
        """Returns class representing nodeeditor content"""
        return self.__class__.NodeContent_class

    def getGraphicsNodeClass(self):
        return self.__class__.GraphicsNode_class
