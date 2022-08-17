import os

from qtpy.QtCore import Qt, QRectF
from qtpy.QtGui import QImage
from qtpy.QtWidgets import QLineEdit, QVBoxLayout
import FreeCAD as App

from nodeeditor.node_node import Node
from nodeeditor.node_socket import LEFT_CENTER, RIGHT_CENTER
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from fcn_conf import register_node, OP_NODE_OBJ_IN
from nodeeditor.utils import dumpException


class ObjectInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.edit = QLineEdit("Label", self)
        self.edit.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.edit)

    def serialize(self):
        res = super().serialize()
        res['label'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['label']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


class ObjectInputGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 75
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        status_icon = os.path.join(App.getUserAppDataDir(), "Macro", "pyqt-node-editor", "examples",
                                   "example_freecad", "icons", "status_icons.png")
        self.icons = QImage(status_icon)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24.0
        if self.node.isDirty(): offset = 0.0
        if self.node.isInvalid(): offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )


@register_node(OP_NODE_OBJ_IN)
class ObjectInputNode(Node):
    icon = os.path.join(os.path.abspath(__file__), "..", "..", "icons", "fcn_default.png")
    op_code = OP_NODE_OBJ_IN
    op_title = "Object"
    content_label_objname = "obj_input_node"

    GraphicsNode_class = ObjectInputGraphicsNode
    NodeContent_class = ObjectInputContent

    def __init__(self, scene):
        super().__init__(scene, self.__class__.op_title, inputs=[], outputs=[3])
        self.value = None
        self.markDirty()
        #self.eval()

    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

    def initInnerClasses(self):
        self.content = ObjectInputContent(self)
        self.grNode = ObjectInputGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

    def eval(self):
        if not self.isDirty() and not self.isInvalid():
            print(" _> returning cached %s value:" % self.__class__.__name__, self.value)
            return self.value
        try:
            val = self.evalImplementation()
            return val
        except ValueError as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantsDirty()
        except Exception as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            #dumpException(e)

    def evalImplementation(self):
        obj_label = self.content.edit.text()
        self.value = self.evalOperation(obj_label)
        self.markDirty(False)
        self.markInvalid(False)
        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()
        self.grNode.setToolTip("")
        self.evalChildren()
        print("%s::__eval()" % self.__class__.__name__, "self.value = ", self.value)
        return self.value

    def evalOperation(self, obj_label):
        if not(App.ActiveDocument is None):
            obj_list = App.ActiveDocument.getObjectsByLabel(obj_label)
            if len(obj_list) == 1:
                return obj_list[0]
            else:
                raise ValueError('Unknown object')
        else:
            raise Exception('No active document')

    def onInputChanged(self, socket=None):
        self.markDirty()
        self.eval()
        print("%s::__onInputChanged" % self.__class__.__name__, "self.value = ", self.value)

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        #print("Deserialized Node '%s'" % self.__class__.__name__, "res:", res)
        return res