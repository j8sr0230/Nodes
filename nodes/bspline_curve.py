import os

from qtpy.QtCore import Qt, QRectF
from qtpy.QtGui import QImage
from qtpy.QtWidgets import QLabel, QVBoxLayout
import FreeCAD as App
import Part

from nodeeditor.node_node import Node
from nodeeditor.node_socket import LEFT_CENTER, RIGHT_CENTER
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from fcn_conf import register_node, OP_NODE_BSPLINE_CRV
from nodeeditor.utils import dumpException


class BSplineCurveGraphicsContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.lbl = QLabel(self.node.content_label, self)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setObjectName(self.node.content_label_objname)
        self.layout.addWidget(self.lbl)


class BSplineCurveGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 95
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


@register_node(OP_NODE_BSPLINE_CRV)
class BSplineCurveNode(Node):
    icon = os.path.join(App.getUserAppDataDir(), "Macro", "pyqt-node-editor", "examples",
                        "example_freecad", "icons", "freecad_default_icon.png")
    op_code = OP_NODE_BSPLINE_CRV
    op_title = "BSpline Curve"
    content_label_objname = "bspline_crv_node"
    content_label = "Crv"

    GraphicsNode_class = BSplineCurveGraphicsNode
    NodeContent_class = BSplineCurveGraphicsContent

    def __init__(self, scene):
        super().__init__(scene, self.__class__.op_title, inputs=[1], outputs=[4])
        self.value = None
        self.input_multi_edged = True
        self.output_multi_edged = True
        self.initSockets([1], [4], True)
        self.markDirty()
        #self.eval()

    def initInnerClasses(self):
        self.content = BSplineCurveGraphicsContent(self)
        self.grNode = BSplineCurveGraphicsNode(self)

    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

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
            dumpException(e)

    def evalImplementation(self):
        inp_list = self.getInputs(0)

        if len(inp_list)==0:
            self.markInvalid()
            self.markDescendantsDirty()
            self.grNode.setToolTip("Connect all inputs")
            return None

        else:
            vec_list = []
            for elem in inp_list:
                vec_list.append(elem.eval())

            val = self.evalOperation(vec_list)
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.grNode.setToolTip("")
            self.markDescendantsDirty()
            self.evalChildren()
            print("%s::__eval()" % self.__class__.__name__, "self.value = ", self.value)
            return val

    def evalOperation(self, vec_list):
        if len(vec_list) > 1:
            shp = Part.BSplineCurve(vec_list).toShape()
            return shp
        else:
            raise ValueError('Missing vectors')

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