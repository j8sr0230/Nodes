import os

from qtpy.QtCore import Qt, QRectF
from qtpy.QtGui import QImage
from qtpy.QtWidgets import QLabel, QVBoxLayout, QFormLayout, QLayout, QPushButton, QHBoxLayout, QLineEdit, QComboBox
import FreeCAD as App

from nodeeditor.node_node import Node
from nodeeditor.node_socket import LEFT_CENTER, RIGHT_CENTER, LEFT_BOTTOM, RIGHT_BOTTOM
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from fcn_conf import register_node, OP_NODE_VEC_XYZ_IN
from nodeeditor.utils import dumpException


class VecXYZInGraphicsContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.input_rows = [
            self.createLabeledInputRow(self.layout, "X", str(1)),
            self.createLabeledInputRow(self.layout, "Y", str(0)),
            self.createLabeledInputRow(self.layout, "Z", str(0))
        ]
        self.output_rows = [self.createLabeledOutputRow(self.layout, "Vec")]

    def createLabeledInputRow(self, form_layout: QFormLayout, label: str = "Input",
                              default_text: str = "Text") -> QLineEdit:
        """Adds a row to an existing QFormLayout, consisting of input label and QLineEdit input field.

        :param form_layout: Existing layout to which the row is added
        :type form_layout: QFormLayout
        :param label: Label of the input row
        :type label: str
        :param default_text: Default text of the QLineEdit
        :type default_text: str
        :return: The generated line edit
        :rtype: QLineEdit
        """
        label = QLabel(label)
        line_edit = QLineEdit(default_text, self)
        form_layout.addRow(label, line_edit)
        return (label, line_edit)

    def createLabeledOutputRow(self, form_layout: QFormLayout, label: str = "Output") -> QLabel:
        """Adds a row to an existing QFormLayout with an output label.

        :param form_layout: Existing layout to which the row is added
        :type form_layout: QFormLayout
        :param label: Label of the output row
        :type label: str
        """
        label = QLabel(label, self)
        label.setAlignment(Qt.AlignRight)
        form_layout.addRow(label)
        return label

    def serialize(self):
        res = super().serialize()
        res['vector'] = {'x': self.input_rows[0][1].text(),
                         'y': self.input_rows[1][1].text(),
                         'z': self.input_rows[2][1].text()}
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            x_value = data['vector']['x']
            self.input_rows[0][1].setText(x_value)
            y_value = data['vector']['y']
            self.input_rows[1][1].setText(y_value)
            z_value = data['vector']['z']
            self.input_rows[2][1].setText(z_value)
        except Exception as e:
            dumpException(e)
        return res


class VecXYZInGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 95
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initUI(self):
        super().initUI()
        self.width = self.content.width()
        self.height = self.content.height() + self.title_height

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


@register_node(OP_NODE_VEC_XYZ_IN)
class VecXYZInNode(Node):
    icon = os.path.join(App.getUserAppDataDir(), "Macro", "pyqt-node-editor", "examples",
                        "example_freecad", "icons", "freecad_default_icon.png")
    op_code = OP_NODE_VEC_XYZ_IN
    op_title = "Vector In"
    #content_label_objname = "vec_xyz_in_node"
    #content_label = ""

    GraphicsNode_class = VecXYZInGraphicsNode
    NodeContent_class = VecXYZInGraphicsContent

    def __init__(self, scene):
        super().__init__(scene, self.__class__.op_title, inputs=[0, 0, 0], outputs=[1])
        self.value = None
        self.markDirty()
        self.eval()

    def initInnerClasses(self):
        self.content = VecXYZInGraphicsContent(self)
        self.grNode = VecXYZInGraphicsNode(self)

        self.content.input_rows[0][1].textChanged.connect(self.onInputChanged)
        self.content.input_rows[1][1].textChanged.connect(self.onInputChanged)
        self.content.input_rows[2][1].textChanged.connect(self.onInputChanged)


    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_BOTTOM
        self.output_socket_position = RIGHT_BOTTOM

    def getSocketPosition(self, index: int, position: int, num_out_of: int = 1) -> '(x, y)':
        x, y = super().getSocketPosition(index, position, num_out_of)

        if position == LEFT_BOTTOM:
            elem = self.content.input_rows[index][1]
            y = 0.5 + self.grNode.title_height + (
                    elem.geometry().height() // 2) + elem.geometry().topLeft().y() - self.content.layout.geometry().topLeft().y()
        elif position == RIGHT_BOTTOM:
            elem = self.content.output_rows[index]
            y = 0.5 + self.grNode.title_height + (
                    elem.geometry().height() / 2) + elem.geometry().topLeft().y() - self.content.layout.geometry().topLeft().y()
        return [x, y]

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
        x = self.getInput(0)
        y = self.getInput(1)
        z = self.getInput(2)

        if x is not None:
            x_val = x.eval()
            self.content.input_rows[0][1].setText(str(x_val))
        else:
            x_val = float(self.content.input_rows[0][1].text())

        if y is not None:
            y_val = y.eval()
            self.content.input_rows[1][1].setText(str(y_val))
        else:
            y_val = float(self.content.input_rows[1][1].text())

        if z is not None:
            z_val = z.eval()
            self.content.input_rows[2][1].setText(str(z_val))
        else:
            z_val = float(self.content.input_rows[2][1].text())

        val = self.evalOperation(x_val, y_val, z_val)
        self.value = val
        self.markDirty(False)
        self.markInvalid(False)
        self.grNode.setToolTip("")
        self.markDescendantsDirty()
        self.evalChildren()
        print("%s::__eval()" % self.__class__.__name__, "self.value = ", self.value)
        return val

    def evalOperation(self, x, y, z):
        vector = App.Vector(x, y, z)
        if vector:
            return vector
        else:
            raise ValueError('Wrong input values')

    def onInputChanged(self, socket=None):
        self.markDirty()
        self.eval()
        print("%s::__onInputChanged" % self.__class__.__name__, "self.value = ", self.value)

    def onEdgeConnectionChanged(self, new_edge: 'Edge'):
        """
        Event handling that any connection (`Edge`) has changed.

        :param new_edge: reference to the changed :class:`~nodeeditor.node_edge.Edge`
        :type new_edge: :class:`~nodeeditor.node_edge.Edge`
        """
        if new_edge.end_socket != None:
            if new_edge.end_socket.node == self:
                # New edge in input
                input_elem = self.content.input_rows[new_edge.end_socket.index][1]
                input_elem.setText(str(self.getInput(new_edge.end_socket.index).eval()))
                input_elem.setDisabled(True)
            else:
                # New edge on output
                pass
        else:
            # Edge on input or output deleted
            for socket in self.inputs:
                if not socket.hasAnyEdge():
                    input_elem = self.content.input_rows[socket.index][1]
                    input_elem.setDisabled(False)

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        #print("Deserialized Node '%s'" % self.__class__.__name__, "res:", res)
        return res