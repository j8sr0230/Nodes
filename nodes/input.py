import os

from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from fcn_conf import register_node, OP_NODE_INPUT
from fcn_node_base import BaseNode, BaseGraphicsNode


class NumberInputContent(QDMNodeContentWidget):

    edit: QLineEdit

    def initUI(self):
        self.edit = QLineEdit("1", self)
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)

    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap=None, restore_id=True) -> bool:
        if hashmap is None:
            hashmap = {}
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_INPUT)
class NumberInputNode(BaseNode):

    icon = os.path.join(os.path.abspath(__file__), "..", "..",  "icons", "in.png")
    op_code = OP_NODE_INPUT
    op_title = "Input"
    content_label_objname = "calc_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[0])
        self.eval()

    def initInnerClasses(self):
        self.content = NumberInputContent(self)
        self.grNode = BaseGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

    def eval_implementation(self):
        u_value = self.content.edit.text()
        s_value = int(u_value)
        self.value = s_value
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return self.value
