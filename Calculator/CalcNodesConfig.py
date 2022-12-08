from PyQt5.QtCore import Qt
from CalculatorConfig import *
from CalculatorBaseNode import *

@register_node(OP_NODE_ADD)
class CalcNode_Add(CalculatorBaseNodeFunctions):
    #icon = "icons/add.png"
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = "+"
    content_label_objname = "calc_node_bg"


@register_node(OP_NODE_SUB)
class CalcNode_Sub(CalculatorBaseNodeFunctions):
    #icon = "icons/sub.png"
    op_code = OP_NODE_SUB
    op_title = "Substract"
    content_label = "-"
    content_label_objname = "calc_node_bg"

@register_node(OP_NODE_MUL)
class CalcNode_Mul(CalculatorBaseNodeFunctions):
    #icon = "icons/mul.png"
    op_code = OP_NODE_MUL
    op_title = "Multiply"
    content_label = "*"
    content_label_objname = "calc_node_mul"

@register_node(OP_NODE_DIV)
class CalcNode_Div(CalculatorBaseNodeFunctions):
    #icon = "icons/divide.png"
    op_code = OP_NODE_DIV
    op_title = "Divide"
    content_label = "/"
    content_label_objname = "calc_node_div"


class CalcInputContent(CalculatorGraphicalNodeContent):
    def initUI(self):
        self.edit = QLineEdit("1", self)
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)


@register_node(OP_NODE_INPUT)
class CalcNode_Input(CalculatorBaseNodeFunctions):
    #icon = "icons/in.png"
    op_code = OP_NODE_INPUT
    op_title = "Input"
    content_label_objname = "calc_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])

    def getInnerClasses(self):
        node_content_class = self.getNodeContentClass()
        graphics_node_class = self.getGraphicsNodeClass()

class CalcOutputContent(CalculatorGraphicalNodeContent):
    def initUI(self):
        self.lbl = QLabel("42", self)
        self.lbl.setAlignment(Qt.AlignLeft)
        self.lbl.setObjectName(self.node.content_label_objname)

@register_node(OP_NODE_OUTPUT)
class CalcNode_Output(CalculatorBaseNodeFunctions):
    #icon = "icons/out.png"
    op_code = OP_NODE_OUTPUT
    op_title = "Output"
    content_label_objname = "calc_node_output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])

    def getInnerClasses(self):
        node_content_class = self.getNodeContentClass()
        graphics_node_class = self.getGraphicsNodeClass()



# way how to register by function call
# register_node_now(OP_NODE_ADD, CalcNode_Add)
