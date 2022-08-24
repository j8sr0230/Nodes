# -*- coding: utf-8 -*-
"""Base node template for FreeCAD Nodes (fc_nodes).

Author: R. Scharf-Wildenhain (j8sr0230), 19.08.2022
Licence: LGPL-2.1
Website: https://github.com/j8sr0230/fc_nodes

This module contains all necessary classes to create custom nodes for the visual
modeling environment FreeCAD Nodes (fc_nodes). It contains the classes:
- FCNGraphicsSocket (socket visualization) and FCNSocket (socket model),
- FCNGraphicsNode (node visualization) and FCNNode (node model) and
- FCNContent (node content visualization)
for the complete graphical and logical implementation of individual nodes.

It uses significantly the modules QtPy as abstraction layer for PyQt5 and PySide2
(https://pypi.org/project/QtPy/, MIT license) and the pyqt-node-editor by Pavel
Křupala (https://gitlab.com/pavel.krupala/pyqt-node-editor, MIT license) as node
editor base framework.
"""

import os
from collections import OrderedDict
from typing import Union

from qtpy.QtGui import QImage
from qtpy.QtCore import QRectF, Qt
from qtpy.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QSlider, QComboBox
from nodeeditor.node_node import Node
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_socket import Socket, LEFT_BOTTOM, RIGHT_BOTTOM
from nodeeditor.node_graphics_socket import QDMGraphicsSocket
from fcn_conf import register_node, OP_NODE_BASE
from nodeeditor.utils import dumpException


class FCNGraphicsSocket(QDMGraphicsSocket):
    """Visual representation of a socket in a node editor scene.

    The visual representation of the sockets consists of a label and an input/
    display widget. For connected sockets, the input/display widget shows the
    corresponding input value. For free sockets, the socket value can be
    entered directly via this widget. This class holds the visual elements of
    a socket consisting of a socket label (QLabel) and an input/display
    widget (QWidget). All available input/display elements are stored in the
    class variable Socket_Input_Widget_Classes as a list. The selection of
    an explicit input element from the list Socket_Input_Widget_Classes is done
    dynamically during FCNSocket initialisation.

    Attributes:
        label_widget (QLabel): Visual socket label.
        input_widget (QWidget): Visual socket input element.
    """

    Socket_Input_Widget_Classes: list = [QLabel, QLineEdit, QSlider, QComboBox]

    label_widget: QLabel
    input_widget: QWidget

    def init_inner_widgets(self, socket_label: str = "", socket_input_index: int = 0,
                           socket_default_values: Union[int, str, list] = 0):
        """Generates the ui widgets for socket label and input.

        This method is called by the FCNSocket class and creates the visual socket
        label and the input widget specified by the socket_input_index and
        socket_default_value. In addition to the label alignment, specific settings
        for the selected input widget is made.
        :param socket_label: Label of the socket.
        :type socket_label: str
        :param socket_input_index: Index of input class, referring to the Socket_Input_Classes list.
        :type socket_input_index: int
        :param socket_default_values: Socket widget default data object.
        :type socket_default_values: object
        """

        # Socket label setup
        self.label_widget = QLabel(socket_label)
        if self.socket.is_input:
            self.label_widget.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        else:
            self.label_widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Socket input widget setup
        self.input_widget = self.__class__.Socket_Input_Widget_Classes[socket_input_index]()
        if socket_input_index == 0:  # Empty
            pass

        elif socket_input_index == 1:  # QLineEdit
            self.input_widget.setText(str(socket_default_values))
            self.input_widget.textChanged.connect(self.socket.node.onInputChanged)

        elif socket_input_index == 2:  # QSlider
            self.input_widget.setOrientation(Qt.Horizontal)
            self.input_widget.setMinimum(0)
            self.input_widget.setMaximum(100)
            self.input_widget.setValue(int(socket_default_values))
            self.input_widget.valueChanged.connect(self.socket.node.onInputChanged)

        elif socket_input_index == 3:  # QComboBox
            for text in socket_default_values:
                self.input_widget.addItem(text)
            self.input_widget.currentIndexChanged.connect(self.socket.node.onInputChanged)

    def update_widget_value(self):
        """Updates the value shown by the socket input widget.

        Socket input/display widgets work in two directions. If no node is
        connected to the socket, they serve for quick manipulation of the
        respective socket input value, i.e. the serve as an input field.
        However, if a node is connected to the socket, they will show the
        input value passed through that node. This method evaluates the
        connected node and displays the corresponding value in the input/
        display widget.

        Note:
            The update_widget_value method is limited to sockets with one
            connection.
        """

        if self.socket.hasAnyEdge() and len(self.socket.edges) == 1:
            # If socket is connected with just one edge
            connected_node = self.socket.node.getInput(self.socket.index)
            connected_output_index = self.socket.edges[0].getOtherSocket(self.socket).index
            print("Connected node:", connected_node, "on output socket:", connected_output_index)

            if isinstance(self.input_widget, QLineEdit):
                self.input_widget.setText(str(connected_node.eval(connected_output_index)))
            elif isinstance(self.input_widget, QSlider):
                self.input_widget.setValue(int(connected_node.eval(connected_output_index)))
            elif isinstance(self.input_widget, QComboBox):
                self.input_widget.setCurrentIndex(int(connected_node.eval(connected_output_index)))

    def update_widget_status(self):
        """Updates the input widget state (enabled or disabled).

        In addition to the update_widget_value method, the input/display widget
        of a connected socket is disabled by this update_widget_status method.
        """

        if self.socket.hasAnyEdge():
            # If socket is connected
            self.input_widget.setDisabled(True)
            self.update_widget_value()
        else:
            self.input_widget.setDisabled(False)


class FCNSocket(Socket):
    """Model class for an input or output socket of a node.

    Each node has input and output sockets for communication with other nodes.
    A socket is the data interface between two nodes. They are connected to
    sockets from other nodes via edges and thus ensure the data flow in the node
    graph. This class has the Socket_GR_Class class variable that defines the
    user interface class for the FCNSocket. The class name FCNGraphicsSocket is
    passed to it. In addition to the inherited methods and parameters, FCNSocket
    essentially has a socket_label to name the socket, a socket_input_index to
    identify the desired input widget and a socket_default_value.
    """

    Socket_GR_Class = FCNGraphicsSocket

    socket_label: str
    socket_input_index: int
    socket_default_value: object

    def __init__(self, node: Node, index: int = 0, position: int = LEFT_BOTTOM, socket_type: int = 1,
                 multi_edges: bool = True, count_on_this_node_side: int = 1, is_input: bool = False,
                 socket_label: str = "", socket_input_index: int = 0, socket_default_value: object = 0):
        """Constructor of the FCNGraphicsSocket class.

        :param node: Parent node of the socket.
        :type node: Node
        :param index: Current index of this socket in the position.
        :type index: int
        :param position: Initial position of the socket, referring to node_sockets.py.
        :type position: int
        :param socket_type: Type (color) the socket.
        :type socket_type: int
        :param multi_edges: Can this socket handle multiple edges input?
        :type multi_edges: bool
        :param count_on_this_node_side: Total number of sockets on this position.
        :type count_on_this_node_side: int
        :param is_input: Is this an input socket?
        :type is_input: bool
        :param socket_label: Socket label
        :type socket_label: str
        :param socket_input_index: Index of input class, referring to the
        FCNGraphicsSocket.Socket_Input_Classes list.
        :type socket_input_index: int
        :param socket_default_value: Default value of the socket input widget.
        :type socket_input_index: object
        """

        super().__init__(node, index, position, socket_type, multi_edges, count_on_this_node_side, is_input)
        self.socket_label = socket_label
        self.socket_input_index = socket_input_index
        self.socket_default_value = socket_default_value
        self.grSocket.init_inner_widgets(self.socket_label, self.socket_input_index, self.socket_default_value)


class FCNGraphicsNode(QDMGraphicsNode):
    """Visual representation of a node in a node editor scene.

    The visual node is a QGraphicsItem that is display in a QGraphicsScene instance.
    In addition, it serves as a container for the visual node content (see
    FCNNodeContent class).The FCNGraphicsNode class specifies all the necessary
    geometric information needed, to display a node in the scene.

    Attributes:
        width (int): Width of the node.
        height (int): Height of the node.
        edge_roundness (int): Roundness of the node corners.
        edge_padding (int): Padding between node and node content.
        title_horizontal_padding (int): Horizontal padding between node and node title.
        title_vertical_padding (int): Vertical padding between node and node title.
        icons (QImage): Status icons of the node, that is displayed in the top left corner.
    """

    width: int
    height: int
    edge_roundness: int
    edge_padding: int
    title_horizontal_padding: int
    title_vertical_padding: int
    icons: QImage

    def initSizes(self):
        """Initialises the size of the visual node.

        This method sets the class attributes for the node dimensions and content
        paddings.
        """

        super().initSizes()
        self.width = 250
        self.height = 230
        self.edge_roundness = 6
        self.edge_padding = 10
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        """Initialises the status icons of the node.

        Status icons indicate whether a node is valid, invalid or dirty. This method sets
        the class attribute for the status icons.
        """

        super().initAssets()
        path = os.path.join(os.path.abspath(__file__), "../..", "icons", "status_icons.png")
        self.icons = QImage(path)

    def paint(self, painter, q_style_option_graphics_item, widget=None):
        """Paints the appropriate status icons on the visual node representation.

       Status icons indicate whether a node is valid, invalid or dirty. All status
       icons are in a single landscape image. A corresponding horizontal offset is
       used to select the required image section via this offset. This method
       selects and draws the corresponding image section through the QPainter instance.
       """
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
    """The visual representation of the node content.

    The visual node content is composed by the labels and input widgets passed
    by the initialised input and output sockets. All widgets are arranged row wise
    by a QFormLayout and stored in class attributes. Widgets of input sockets are
    stored in the input_widgets list and widgets of output sockets are passed to
    the output_widgets list.

    Attributes:
        input_widgets (list[QWidget]): Input widgets of the input sockets.
        output_widgets (list[QWidget]): Output widgets of the output sockets.
        layout (QFormLayout): Layout of the node content widget.
    """

    input_widgets: list
    output_widgets: list
    layout: QFormLayout

    def initUI(self):
        """Initializes the node content user interface layout.

       The initUI method initializes and sets the layout of the content widget
       as a QFormLayout. It is called by the contractor of the parent class
       QDMNodeContentWidget.
       """

        self.hide()  # Hack: Needed for updating widget geometry
        self.layout = QFormLayout(self)
        self.setLayout(self.layout)

    def fill_content_layout(self):
        """Populates the content layout with socket labels and widgets.

        This method loops over all present input and output sockets af the parent
        node. Labels and input widgets are added to the QFormLayout and references
        the input widgets are saved in the class attribute lists. Widgets of input
        sockets are passed to the input_widgets list and widgets of output sockets
        are stored in the output_widget list. To query the individual sockets, they
        must already be initiated.

        Note:
            For this reason the call of this methode does not take place in the
            initUI method of this class, but in the constructor of the FCNNode
            class after initiation of the Node parent class.
       """

        self.input_widgets = []
        self.output_widgets = []

        for socket in self.node.inputs:
            self.input_widgets.append(socket.grSocket.input_widget)
            self.layout.addRow(socket.grSocket.label_widget, socket.grSocket.input_widget)

        for socket in self.node.outputs:
            self.output_widgets.append(socket.grSocket.label_widget)
            self.layout.addRow(socket.grSocket.input_widget, socket.grSocket.label_widget)

        self.show()  # Hack: Needed for updating widget geometry

    def serialize(self) -> OrderedDict:
        """Serialises the node content to human-readable json file.

        The serialise method adds the content (int, float, sting, ...) of each
        socket widget to a dictionary and returns it. It is called by the serialise
        method of the parent node.

        :return: Serialised date as human-readable json file.
        :rtype: OrderedDict
        """
        res = super().serialize()

        for idx, widget in enumerate(self.input_widgets):
            if isinstance(widget, QLineEdit):
                res["widget" + str(idx)] = str(widget.text())
            elif isinstance(widget, QSlider):
                res["widget" + str(idx)] = str(widget.value())
            elif isinstance(widget, QComboBox):
                res["widget" + str(idx)] = str(widget.currentIndex())
        return res

    def deserialize(self, data: dict, hashmap=None, restore_id: bool = True) -> bool:
        """Deserializes the node content.

        Deserialization method which takes data in dict format with helping
        hashmap containing references to existing entities.

        :param data: Dictionary containing serialized data.
        :type data: dict
        :param hashmap: Helper dictionary containing references (by id == key) to existing objects.
        :type hashmap: dict
        :param restore_id: True if we are creating new content. False is useful when loading existing
            content of which we want to keep the existing object's id.
        :type restore_id: bool
        :return: True if deserialization was successful, otherwise False.
        :rtype: bool
        """

        if hashmap is None:
            hashmap = {}
        res = super().deserialize(data, hashmap)
        try:
            for idx, widget in enumerate(self.input_widgets):
                value = data["widget" + str(idx)]
                if isinstance(widget, QLineEdit):
                    widget.setText(value)
                elif isinstance(widget, QSlider):
                    widget.setValue(int(value))
                elif isinstance(widget, QComboBox):
                    widget.setCurrentIndex(int(value))
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_BASE)
class FCNNode(Node):
    """Data model class for a node in FreeCAD Nodes (fc_nodes).

     The FCNNode class contains the complete data model of a node. All necessary
     information is stored and managed either in class variables or attributes.
     This concerns not only the visual representation of the node in the node editor
     scene including node content and sockets, but also the complete evaluation
     logic.

     General instance independent data are stored in class variables. These are:
     - icon (str): Path to the node image, displayed in the node list box (QListWidget).
     - op_code (int): Unique index of the node, used to register the node in the app,
        referring to fcn_conf.py.
     - op_title (str): Title of the node, display in the node header.
     - content_label_objname (str): Label of the content widget, used by qss stylesheets.
     - GraphicsNode_class (QDMGraphicsNode): Name of node ui class.
     - NodeContent_class (QDMNodeContentWidget): Name of node content ui class.
     - Socket_class (Socket): Name of socket class.

     Attributes:
        input_init_list (list(tuple)): Definition of the input sockets with the signature
            [(socket_type (int), socket_label (str), socket_widget_index (int),
            widget_default_value (obj), multi_edge (bool))]
        output_init_list (list(tuples)): Definition of the output sockets with the signature
            [(socket_type (int), socket_label (str), socket_widget_index (int),
            widget_default_value (obj), multi_edge (bool))]
        content (FCNNodeContent): Reference to the node content widget.
        data (list): Result of the node evaluation, used as cache storage to limit evaluation cycles.
        input_socket_position (int): Initial position of the input sockets, referring to node_sockets.py.
        output_socket_position (int): Initial position of the output sockets, referring to node_sockets.py.

     Note:
        If input_socket_position is set to LEFT_BOTTOM and output_socket_position
        is set to RIGHT_BOTTOM, the socket positions are calculated by the content
        layout based on the input and output widgets of the sockets.
    """

    icon: str = os.path.join(os.path.abspath(__file__), "..", "..", "icons", "fcn_default.png")
    op_code: int = OP_NODE_BASE
    op_title: str = "FCN Node"
    content_label_objname: str = "fcn_node_bg"

    GraphicsNode_class: FCNGraphicsNode = FCNGraphicsNode
    NodeContent_class: FCNNodeContent = FCNNodeContent
    Socket_class: Socket = FCNSocket

    inputs_init_list: list
    output_init_list: list
    content: FCNNodeContent
    data: list
    input_socket_position: int
    output_socket_position: int

    def __init__(self, scene):
        """Constructor of the FCNNode class.

        :param scene: Parent node of the socket.
        :type scene: Scene
        """

        self.inputs_init_list = [(0, "Op", 3, ["Add", "Sub", "Mul", "Div"], True), (0, "Min", 1, 0, True),
                                 (0, "Max", 1, 100, True), (0, "Val", 2, 50, True)]
        self.output_init_list = [(0, "Out 1", 0, 0, True), (0, "Out 2", 0, 0, True)]

        super().__init__(scene, self.__class__.op_title, self.inputs_init_list, self.output_init_list)

        # Init content after parent (and socket initialisation) initiation, because
        # the fill_content_layout method loops over all sockets.
        self.content.fill_content_layout()
        self.place_sockets()  # Adjusts socket position according content widget positions

        self.data = list()
        self.markDirty()
        self.eval()

    def update_content_status(self):
        """Updates the content input widget state (enabled or disabled).

        The input/display widget status of all connected sockets is update by
        this method.
        """

        for socket in self.inputs:
            socket.grSocket.update_widget_status()

    def place_sockets(self):
        """Updates the socket positions.

        Calls the setSocketPosition method of all sockets. It causes all sockets
        to re-fetch their position within the node using the getSocketPosition
        method o this class.
        """

        for socket in self.inputs:
            socket.setSocketPosition()
        for socket in self.outputs:
            socket.setSocketPosition()

    def getSocketPosition(self, index: int, position: int, num_out_of: int = 1) -> [int, int]:
        """Calculates the position of an individual socket within th node geometry.

        Calls the setSocketPosition method of all sockets. It causes all sockets
        to re-fetch their position within the node using the getSocketPosition
        method o this class.

        :param index: Index of the target socket.
        :type index: int
        :param position: Position of the target socket, referring to node_sockets.py.
        :type position: int
        :param num_out_of: Total number of sockets on this position.
        :type num_out_of: int
        :return: Calculated position vector of the socket.
        :rtype: [int, int]
        """

        x, y = super().getSocketPosition(index, position, num_out_of)

        if hasattr(self.content, "input_widgets"):
            # If sockets have already been initiated
            if position == LEFT_BOTTOM:
                elem = self.content.input_widgets[index]
                y = self.grNode.title_vertical_padding + self.grNode.title_height + elem.geometry().topLeft().y() + \
                    (elem.geometry().height() // 2)
            elif position == RIGHT_BOTTOM:
                elem = self.content.output_widgets[index]
                y = self.grNode.title_vertical_padding + self.grNode.title_height + elem.geometry().topLeft().y() + \
                    (elem.geometry().height() // 2)

        return [x, y]

    def initSettings(self):
        """Initiates socket positions.

       The socket positions input_socket_position and output_socket_position are used, to calculate
       the visual socket distribution within the node.

       Note:
           If set to LEFT_BOTTOM and RIGHT_BOTTOM, the position of the socket input widgets within
           the content layout is used, to calculate the socket positions.
       """

        super().initSettings()
        self.input_socket_position = LEFT_BOTTOM
        self.output_socket_position = RIGHT_BOTTOM

    def initSockets(self, inputs: list, outputs: list, reset: bool = True):
        """Create the input and output sockets of the node.

        The initSockets method instantiates the socket data model classes, along
        with the corresponding socket ui classes. All necessary information for
        the individual sockets are passes through the inputs and outputs list to
        the method.

        :param inputs: Definition of the input sockets with the signature
            [(socket_type (int), socket_label (str), socket_widget_index (int),
            widget_default_value (obj), multi_edge (bool))]
        :type inputs: list(tuple)
        :param outputs: Definition of the output sockets with the signature
            [(socket_type (int), socket_label (str), socket_widget_index (int),
            widget_default_value (obj), multi_edge (bool))]
        :type outputs: list(tuple)
        :param reset: True destroys and removes old sockets.
        :type reset: bool
        """

        if reset:
            # Clear old sockets
            if hasattr(self, 'inputs') and hasattr(self, 'outputs'):
                # Remove visual sockets from scene
                for socket in (self.inputs+self.outputs):
                    self.scene.grScene.removeItem(socket.grSocket)
                self.inputs = []
                self.outputs = []

        # Create new sockets
        counter = 0
        for item in inputs:
            socket = self.__class__.Socket_class(
                node=self, index=counter, position=self.input_socket_position,
                socket_type=item[0], multi_edges=item[4],
                count_on_this_node_side=len(inputs), is_input=True, socket_label=item[1], socket_input_index=item[2],
                socket_default_value=item[3]
            )
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = self.__class__.Socket_class(
                node=self, index=counter, position=self.output_socket_position,
                socket_type=item[0], multi_edges=item[4],
                count_on_this_node_side=len(outputs), is_input=False, socket_label=item[1], socket_input_index=item[2],
                socket_default_value=item[3]
            )
            counter += 1
            self.outputs.append(socket)

    def eval(self, index: int = 0) -> object:
        """Top level evaluation method of the node.

        A node evaluates the values for the output sockets based on the input
        socket values and the processing logic of the eval_preparation and
        eval_operation methods. If a node is not dirty or invalid, the cached
        data is returned. Otherwise, a new calculation is delegated to the
        eval_preparation method.

        :param index: Index of the output socket, that is to be evaluated.
        :type index: int
        :return: Result of the evaluation.
        :rtype: object
        """

        if not self.isDirty() and not self.isInvalid():
            # Return cached result or the desired output socket (index)
            print("_> returning cached %s data:" % self.__class__.__name__, self.data)
            return self.data[index]
        try:
            # Run new evaluation and return the desired output socket (index)
            socket_output_data = self.eval_preparation()
            return socket_output_data[index]
        except ValueError as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantsDirty()
        except Exception as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            dumpException(e)

    def eval_preparation(self) -> list:
        """Prepares the evaluation of the output socket values.

        This method prepares the actual calculation of the socket output values.
        Input values are collected from connected nodes or socket input widgets,
        stored in a list data structure and passed to the eval_operation method.
        After successful calculation, this method sends the result back to the
        top level eval method.

        Note:
            All output sockets are evaluated. The resulting data structure is returned
            and passed to the data class attribute.

        :return: Calculated output data structure as list o lists with all socket outputs.
        :rtype: list
        """

        # Collect input date either from all input sockets or from the input widget
        # if possible and generates input data structure
        sockets_input_data = []  # Container for input data

        for socket in self.inputs:
            socket_input_data = []
            socket_input_widget = socket.grSocket.input_widget

            if socket.hasAnyEdge() and len(socket.edges) >= 1:
                # At least one edge connected
                if len(socket.edges) > 1:
                    # More than on edge connected
                    socket_input_widget.hide()
                else:
                    # Exactly one edge connected
                    socket.grSocket.update_widget_status()
                    socket_input_widget.show()
                self.place_sockets()  # Replace socket positions

                # Collect input data from connected nodes
                for edge in socket.edges:
                    other_socket = edge.getOtherSocket(socket)
                    other_socket_node = other_socket.node
                    other_socket_index = other_socket.index
                    other_socket_value = other_socket_node.eval(other_socket_index)
                    socket_input_data.append(other_socket_value)
            else:
                # No edge connected
                # socket_input_data.append(socket.socket_default_value)  # Use default socket data

                # Use input widget data
                socket_input_widget = socket.grSocket.input_widget
                if socket_input_widget is not None:
                    if isinstance(socket_input_widget, QLineEdit):
                        input_value = int(socket_input_widget.text())
                        socket_input_data.append(input_value)
                    elif isinstance(socket_input_widget, QSlider):
                        socket_input_widget.setRange(int(self.content.input_widgets[1].text()),
                                                     int(self.content.input_widgets[2].text()))
                        input_value = int(socket_input_widget.value())
                        socket_input_data.append(input_value)
                    elif isinstance(socket_input_widget, QComboBox):
                        pass
                    else:
                        pass

            sockets_input_data.append(socket_input_data)
        socket_output_data = self.eval_operation(sockets_input_data)

        self.data = socket_output_data
        self.markDirty(False)
        self.markInvalid(False)
        self.grNode.setToolTip("")
        self.markDescendantsDirty()
        self.evalChildren()
        print("%s::__eval()" % self.__class__.__name__, "self.data = ", self.data)
        return socket_output_data

    @staticmethod
    def eval_operation(socket_input_data) -> list:
        """Calculation of the socket output values.

        The eval_operation is responsible or the actual calculation of the output
        values. It processes the input data structure passed in through the method
        parameter socket_input_data and returns the calculation result as a list,
        with one sublist per output socket.

        :param socket_input_data: Socket input values as list data structure.
        :type socket_input_data: list
        :return: Calculated output data as list with one sublist per output socket.
        :rtype: list
        """

        # Example implementation
        out1_val = socket_input_data[1][0]
        out2_val = socket_input_data[2][0]

        return [out1_val, out2_val]

    def onInputChanged(self, socket: FCNSocket = None):
        """Callback method for input changed events.

        Each new data input or connection requires updating the content widgets
        (enabled or disabled) and recalculating the node. This is triggered by
        this callback methode.

        :param socket: Socket trigger of the input change (not implemented yet).
        :type socket: FCNSocket
        """

        super().onInputChanged(socket)
        self.update_content_status()
        self.eval()
        print("%s::__onInputChanged" % self.__class__.__name__, "self.data = ", self.data)

    def serialize(self) -> OrderedDict:
        """Serialises the node to human-readable json file.

        The serialise method adds the node date to a dictionary and returns it.
        It is called by the serialise method of the QGraphicsScene node_scene.Scene.serialize.

        :return: Serialised date as human-readable json file.
        :rtype: OrderedDict
        """

        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data: dict, hashmap=None, restore_id: bool = True, *args, **kwargs) -> bool:
        """Deserializes the node.

        Deserialization method which takes data in dict format with helping
        hashmap containing references to existing entities.

        :param data: Dictionary containing serialized data.
        :type data: dict
        :param hashmap: Helper dictionary containing references (by id == key) to existing objects.
        :type hashmap: dict
        :param restore_id: True if we are creating new content. False is useful when loading existing
            content of which we want to keep the existing object's id.
        :type restore_id: bool
        :return: True if deserialization was successful, otherwise False.
        :rtype: bool
        """

        if hashmap is None:
            hashmap = {}
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized Node '%s'" % self.__class__.__name__, "res:", res)
        return res
