import os

from qtpy.QtGui import QImage
from qtpy.QtCore import QRectF, Qt
from qtpy.QtWidgets import QWidget, QLabel, QLineEdit, QSlider
from nodeeditor.node_node import Node
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_socket import Socket, LEFT_TOP, LEFT_CENTER, LEFT_BOTTOM, RIGHT_CENTER, RIGHT_BOTTOM
from nodeeditor.node_graphics_socket import QDMGraphicsSocket
from fcn_conf import register_node, OP_NODE_BASE
from nodeeditor.utils import dumpException


DEBUG = True


class FCNGraphicsSocket(QDMGraphicsSocket):
    """Visual representation of socket in scene."""

    Socket_Input_Widget_Classes = [QLineEdit, QSlider]

    def __init__(self, socket: Socket = None):
        """
        :param socket: Socket model for visual representation
        :type socket: Socket
        """
        super().__init__(socket)
        self.label_widget = None
        self.input_widget = None

    def init_inner_widgets(self, socket_label, socket_input_index):
        """
        Initiates socket label and input widget.

        :param socket_label: Label of the socket
        :type socket_label: str
        :param socket_input_index: Index of input class, referring to the Socket_Input_Classes list
        :type socket_input_index: int
        """
        self.label_widget = QLabel(socket_label)
        if self.socket.is_input:
            self.label_widget.setAlignment(Qt.AlignLeft)
        else:
            self.label_widget.setAlignment(Qt.AlignRight)

        self.input_widget = self.__class__.Socket_Input_Widget_Classes[socket_input_index]()
        if socket_input_index == 0:  # QLineEdit
            self.input_widget.setText("Input")
        elif socket_input_index == 1:  # QSlider
            self.input_widget.setValue(1)

        if DEBUG:
            print(self.label_widget, self.input_widget)


class FCNSocket(Socket):
    """Modified socket class with socket label and input widget."""

    Socket_GR_Class = FCNGraphicsSocket

    def __init__(self, node: Node, index: int = 0, position: int = LEFT_TOP, socket_type: int = 1,
                 multi_edges: bool = True, count_on_this_node_side: int = 1, is_input: bool = False,
                 socket_label: str = "", socket_input_index: int = 0):
        """
        :param node: Parent node of the socket
        :type node: Node
        :param index: Current index of this socket in the position
        :type index: int
        :param position: Socket position
        :type position: int
        :param socket_type: Type (color) of this socket
        :type socket_type: int
        :param multi_edges: Can this socket handle multiple edges input
        :type multi_edges: bool
        :param count_on_this_node_side: Total number of sockets on this position
        :type count_on_this_node_side: int
        :param is_input: Is this an input socket
        :type is_input: bool
        :param socket_label: Socket label
        :type socket_label: str
        :param socket_input_index: Index of input class, referring to the Socket.Socket_Input_Classes list
        :type socket_input_index: int
        """
        super().__init__(node, index, position, socket_type, multi_edges, count_on_this_node_side, is_input)
        self.socket_label = socket_label
        self.socket_input_index = socket_input_index
        self.grSocket.init_inner_widgets(self.socket_label, self.socket_input_index)


class FCNGraphicsNode(QDMGraphicsNode):
    height: int
    width: int
    edge_roundness: int
    edge_padding: int
    title_horizontal_padding: int
    title_vertical_padding: int
    icons: QImage
    input_socket_position: int
    output_socket_position: int

    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        path = os.path.join(os.path.abspath(__file__), "../..", "icons", "status_icons.png")
        self.icons = QImage(path)

    def paint(self, painter, q_style_option_graphics_item, widget=None):
        super().paint(painter, q_style_option_graphics_item, widget)

        offset = 24.0
        if self.node.isDirty():
            offset = 0.0
        if self.node.isInvalid():
            offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )


class FCNNodeContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)


@register_node(OP_NODE_BASE)
class FCNNode(Node):
    icon = os.path.join(os.path.abspath(__file__), "..", "..", "icons", "freecad_default_icon.png")
    op_code = OP_NODE_BASE
    op_title = "FCN Node"
    content_label_objname = "calc_node_bg"
    content_label = "Lbl"

    GraphicsNode_class = FCNGraphicsNode
    NodeContent_class = FCNNodeContent
    Socket_class = FCNSocket

    def __init__(self, scene):
        super().__init__(scene, self.__class__.op_title, inputs=[(0, "In 1", 0), (0, "In 2", 0), (0, "In 3", 0)],
                         outputs=[(1, "Out 1", 1)])
        self.value = None
        self.markDirty()
        self.eval()
        print("Init")

    def initInnerClasses(self):
        self.content = FCNNodeContent(self)
        self.grNode = FCNGraphicsNode(self)
        #self.content.input_rows[0][1].textChanged.connect(self.onInputChanged)
        #self.content.input_rows[1][1].textChanged.connect(self.onInputChanged)
        #self.content.input_rows[2][1].textChanged.connect(self.onInputChanged)

    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_BOTTOM
        self.output_socket_position = RIGHT_BOTTOM

    #def getSocketPosition(self, index: int, position: int, num_out_of: int = 1) -> '(x, y)':
        # x, y = super().getSocketPosition(index, position, num_out_of)
        #
        # if position == LEFT_BOTTOM:
        #     elem = self.content.input_rows[index][1]
        #     y = 0.5 + self.grNode.title_height + (
        #             elem.geometry().height() // 2) + elem.geometry().topLeft().y() - self.content.layout.geometry().topLeft().y()
        # elif position == RIGHT_BOTTOM:
        #     elem = self.content.output_rows[index]
        #     y = 0.5 + self.grNode.title_height + (
        #             elem.geometry().height() / 2) + elem.geometry().topLeft().y() - self.content.layout.geometry().topLeft().y()
        # return [x, y]

    def initSockets(self, inputs: list, outputs: list, reset: bool=True):
        """
        Create sockets for inputs and outputs

        :param inputs: list of Socket Types (int)
        :type inputs: ``list``
        :param outputs: list of Socket Types (int)
        :type outputs: ``list``
        :param reset: if ``True`` destroys and removes old `Sockets`
        :type reset: ``bool``
        """

        if reset:
            # clear old sockets
            if hasattr(self, 'inputs') and hasattr(self, 'outputs'):
                # remove grSockets from scene
                for socket in (self.inputs+self.outputs):
                    self.scene.grScene.removeItem(socket.grSocket)
                self.inputs = []
                self.outputs = []

        # create new sockets
        counter = 0
        for item in inputs:
            socket = self.__class__.Socket_class(
                node=self, index=counter, position=self.input_socket_position,
                socket_type=item[0], multi_edges=self.input_multi_edged,
                count_on_this_node_side=len(inputs), is_input=True, socket_label=item[1], socket_input_index=item[2]
            )
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = self.__class__.Socket_class(
                node=self, index=counter, position=self.output_socket_position,
                socket_type=item[0], multi_edges=self.output_multi_edged,
                count_on_this_node_side=len(outputs), is_input=False, socket_label=item[1], socket_input_index=item[2]
            )
            counter += 1
            self.outputs.append(socket)

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
        print(self.inputs[0].grSocket.label_widget.text())
        pass
        # x = self.getInput(0)
        # y = self.getInput(1)
        # z = self.getInput(2)
        #
        # if x is not None:
        #     x_val = x.eval()
        #     self.content.input_rows[0][1].setText(str(x_val))
        # else:
        #     x_val = float(self.content.input_rows[0][1].text())
        #
        # if y is not None:
        #     y_val = y.eval()
        #     self.content.input_rows[1][1].setText(str(y_val))
        # else:
        #     y_val = float(self.content.input_rows[1][1].text())
        #
        # if z is not None:
        #     z_val = z.eval()
        #     self.content.input_rows[2][1].setText(str(z_val))
        # else:
        #     z_val = float(self.content.input_rows[2][1].text())
        #
        # val = self.evalOperation(x_val, y_val, z_val)
        # self.value = val
        # self.markDirty(False)
        # self.markInvalid(False)
        # self.grNode.setToolTip("")
        # self.markDescendantsDirty()
        # self.evalChildren()
        # print("%s::__eval()" % self.__class__.__name__, "self.value = ", self.value)
        # return val
        return None

    # def evalOperation(self, x, y, z):
    #     vector = App.Vector(x, y, z)
    #     if vector:
    #         return vector
    #     else:
    #         raise ValueError('Wrong input values')

    def onInputChanged(self, socket=None):
        pass
        self.markDirty()
        self.eval()
        print("%s::__onInputChanged" % self.__class__.__name__, "self.value = ", self.value)

    # def onEdgeConnectionChanged(self, new_edge: 'Edge'):
    #     """
    #     Event handling that any connection (`Edge`) has changed.
    #
    #     :param new_edge: reference to the changed :class:`~nodeeditor.node_edge.Edge`
    #     :type new_edge: :class:`~nodeeditor.node_edge.Edge`
    #     """
    #     if new_edge.end_socket != None:
    #         if new_edge.end_socket.node == self:
    #             # New edge in input
    #             input_elem = self.content.input_rows[new_edge.end_socket.index][1]
    #             input_elem.setText(str(self.getInput(new_edge.end_socket.index).eval()))
    #             input_elem.setDisabled(True)
    #         else:
    #             # New edge on output
    #             pass
    #     else:
    #         # Edge on input or output deleted
    #         for socket in self.inputs:
    #             if not socket.hasAnyEdge():
    #                 input_elem = self.content.input_rows[socket.index][1]
    #                 input_elem.setDisabled(False)
    #
    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        # print("Deserialized Node '%s'" % self.__class__.__name__, "res:", res)
        return res