import os

from qtpy.QtWidgets import QLabel
from qtpy.QtCore import Qt
from nodeeditor.node_content_widget import QDMNodeContentWidget

from fcn_conf import register_node, OP_NODE_OUTPUT
from fcn_node_base import BaseNode, BaseGraphicsNode


class NumberOutputContent(QDMNodeContentWidget):

    lbl: QLabel

    def initUI(self):
        self.lbl = QLabel("42", self)
        self.lbl.setAlignment(Qt.AlignLeft)
        self.lbl.setObjectName(self.node.content_label_objname)


@register_node(OP_NODE_OUTPUT)
class NumberOutputNode(BaseNode):

    icon = os.path.join(os.path.abspath(__file__), "..", "..",  "icons", "out.png")
    op_code = OP_NODE_OUTPUT
    op_title = "Output"
    content_label_objname = "calc_node_output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])

    def initInnerClasses(self):
        self.content = NumberOutputContent(self)
        self.grNode = BaseGraphicsNode(self)

    def eval_implementation(self):
        input_node = self.getInput(0)
        if not input_node:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return

        val = input_node.eval()

        if val is None:
            self.grNode.setToolTip("Input is NaN")
            self.markInvalid()
            return

        self.content.lbl.setText("%d" % val)
        self.markInvalid(False)
        self.markDirty(False)
        self.grNode.setToolTip("")

        return val
