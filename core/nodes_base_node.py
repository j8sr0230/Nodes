# -*- coding: utf-8 -*-
###################################################################################
#
#  nodes_base_node.py
#
#  Copyright (c) 2022 Ronny Scharf-Wildenhain <ronny.scharf08@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
###################################################################################
"""Base node module for FreeCAD Nodes (fc_nodes).

This module contains all necessary classes to build custom nodes for the visual modeling environment FreeCAD Nodes
(fc_nodes). It consists of the classes:
- FCNSocketView (socket view) and FCNSocket (socket model),
- FCNContentView (node content view) and
- FCNNodeView (node view) and FCNNode (node model).

It uses significantly the modules QtPy as abstraction layer for PyQt5 and PySide2 (https://pypi.org/project/QtPy, MIT
license) and the pyqt-node-core by Pavel Křupala (https://gitlab.com/pavel.krupala/pyqt-node-editor, MIT license) as
node core base framework.
"""

from collections import OrderedDict
from typing import Union
from math import floor

from qtpy.QtGui import QImage, QTextOption
from qtpy.QtCore import QRectF, Qt
from qtpy.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QSlider, QComboBox, QPlainTextEdit, QSizePolicy

import Exceptions as NodeException;
from nodeeditor.node_scene import Scene
from nodeeditor.node_node import Node
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_socket import Socket, LEFT_BOTTOM, RIGHT_BOTTOM, LEFT_CENTER, RIGHT_CENTER
from nodeeditor.node_graphics_socket import QDMGraphicsSocket
from nodeeditor.utils import dumpException

import nodes_locator as locator

DEBUG = False


class FCNSocketView(QDMGraphicsSocket):
    """Visual representation of a socket in the node core scene.

    All sockets of a node have a label and an input/display widget. If the socket is not connected, the socket input
    value can be manipulated directly via the input widget. For connected sockets, this widget shows a corresponding
    massage, i.e. the input value. This class holds the ui elements for the label (QLabel) and the input/display widget
    (QWidget). All available input/display elements are stored in the class variable Socket_Input_Widget_Classes as a
    list. The selection of an explicit input element from this list is done dynamically during FCNSocket initialisation.

    Attributes:
        label_widget (QLabel): Visual socket label.
        input_widget (QWidget): Visual socket input element.
        mouse_over (bool): Flag for mouse over state.
    """

    Socket_Input_Widget_Classes: list = [QLabel, QLineEdit, QSlider, QComboBox, QPlainTextEdit]

    label_widget: QLabel
    input_widget: QWidget
    mouse_over: bool

    def __init__(self, socket: 'Socket'):
        super().__init__(socket)
        self.mouse_over = False
        self.setAcceptHoverEvents(True)

    def init_inner_widgets(self, socket_label: str = "", socket_input_index: int = 0,
                           socket_default_values: Union[str, int, float, list] = 0):
        """Generates the ui widgets for socket label and input.

        This method is called by the FCNSocket class and creates the visual socket label and the input widget specified
        by the socket_input_index and socket_default_value. In addition to the label alignment, specific settings for
        the selected input widget is made.
        :param socket_label: Label of the socket.
        :type socket_label: str
        :param socket_input_index: Index of input class, referring to the Socket_Input_Classes list.
        :type socket_input_index: int
        :param socket_default_values: Socket widget default data object.
        :type socket_default_values: object
        """

        # Socket label setup
        self.label_widget: QLabel = QLabel(socket_label)
        label_size_policy = self.label_widget.sizePolicy()
        label_size_policy.setVerticalStretch(QSizePolicy.Fixed)
        self.label_widget.setSizePolicy(label_size_policy)

        if self.socket.is_input:
            self.label_widget.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        else:
            self.label_widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Socket input widget setup
        self.input_widget: QWidget = self.__class__.Socket_Input_Widget_Classes[socket_input_index]()
        input_size_policy = self.input_widget.sizePolicy()
        input_size_policy.setVerticalStretch(QSizePolicy.Fixed)
        self.input_widget.setSizePolicy(input_size_policy)

        if socket_input_index == 0:  # Empty
            pass

        elif socket_input_index == 1:  # QLineEdit
            self.input_widget.setText(str(socket_default_values))
            self.input_widget.textChanged.connect(self.socket.node.onInputChanged)

        elif socket_input_index == 2:  # QSlider
            self.input_widget.setOrientation(Qt.Horizontal)
            self.input_widget.setMaximumHeight(20)
            self.input_widget.setMinimum(floor(socket_default_values[0]))
            self.input_widget.setMaximum(floor(socket_default_values[1]))
            self.input_widget.setValue(floor(socket_default_values[2]))
            self.input_widget.valueChanged.connect(self.socket.node.onInputChanged)

        elif socket_input_index == 3:  # QComboBox
            for text in socket_default_values:
                self.input_widget.addItem(text)
            self.input_widget.currentIndexChanged.connect(self.socket.node.onInputChanged)

        elif socket_input_index == 4:  # QPlainTextEdit
            self.input_widget.insertPlainText(str(socket_default_values))
            self.input_widget.textChanged.connect(lambda: self.socket.node.onInputChanged(
                self.input_widget.toPlainText()))
            self.input_widget.setWordWrapMode(QTextOption.NoWrap)

    def hoverEnterEvent(self, event):
        """Handles socket hover events by setting the mouse_over state.

        :param event: A graphics scene hover event.
        :type event: qtpy.QtCore.QEvent
        """

        super().hoverEnterEvent(event)
        self.mouse_over = True

    def hoverLeaveEvent(self, event):
        """Handles socket hover events by setting the mouse_over state.

        :param event: A graphics scene hover event.
        :type event: QEvent
        """

        super().hoverLeaveEvent(event)
        self.mouse_over = False

    def update_widget_status(self):
        """Updates the input widget state.

        In addition to the update_widget_value method, the input/display widget of a connected socket is enabled or
        disabled by the update_widget_status method.
        """

        if self.socket.hasAnyEdge():
            # If socket is connected
            NodeException.nodesInformation("core",self.__class__.__name__,"update_widget_status","hidden")
            self.input_widget.hide()
        else:
            NodeException.nodesInformation("core",self.__class__.__name__,"update_widget_status","shown")
            # self.input_widget.setDisabled(False)
            self.input_widget.show()

    def paint(self, painter, qstyle_option_graphics_item, widget=None):
        """Provides the item’s painting implementation.

        The option parameter provides style options for the item, such as its state, exposed area and its
        level-of-detail hints. The widget argument is optional. If provided, it points to the widget that is being
        painted on; otherwise, it is 0. For cached painting, widget is always 0.

        :param painter: Corresponding QPainter for low-level painting on widgets and other paint devices.
        :type painter: qtpy.QtGui.QPainter
        :param qstyle_option_graphics_item: Style options for the item
        :type qstyle_option_graphics_item: qtpy.QtGui.QStyleOptionGraphicsItem
        :param widget: The widget that is being painted on
        :type widget: qtpy.QtGui.QWidget
        """

        if self.mouse_over:
            self.radius = 7
            self.outline_width = 1
        else:
            self.radius = 6
            self.outline_width = 1

        super().paint(painter, qstyle_option_graphics_item, widget)


class FCNSocket(Socket):
    """Model class for an input or output socket of a node.

    Each node has input and output sockets for communication with other nodes. A socket is the data interface between
    two nodes. They are connected to sockets from other nodes via edges and thus ensure the data flow in the node graph.
    This class has the Socket_GR_Class class variable that defines the user interface class for the FCNSocket. The name
    of the actual Socket ui class is passed to this variable. In this case it's the FCNSocketView. In addition to that,
    FCNSocket instances have a socket_label to name the socket, a socket_input_index to identify the desired input
    widget and the corresponding socket_default_value.
    """

    Socket_GR_Class = FCNSocketView

    socket_label: str
    socket_input_index: int
    socket_default_value: Union[str, int, float, list]

    def __init__(self, node: Node, index: int = 0, position: int = LEFT_BOTTOM, socket_color: int = 1,
                 multi_edges: bool = True, count_on_this_node_side: int = 1, is_input: bool = False,
                 socket_label: str = "", socket_input_index: int = 0, socket_default_value: object = 0,
                 socket_str_type: tuple = None):
        """Constructor of the FCNSocketView class.

        :param node: Parent node of the socket.
        :type node: Node
        :param index: Current index of this socket in the position.
        :type index: int
        :param position: Initial position of the socket, referring to node_sockets.py.
        :type position: int
        :param socket_color: Color the socket.
        :type socket_color: int
        :param multi_edges: Can this socket handle multiple edges input?
        :type multi_edges: bool
        :param count_on_this_node_side: Total number of sockets on this position.
        :type count_on_this_node_side: int
        :param is_input: Is this an input socket?
        :type is_input: bool
        :param socket_label: Socket label
        :type socket_label: str
        :param socket_input_index: Index of input class, referring to the
            FCNSocketView.Socket_Input_Classes list.
        :type socket_input_index: int
        :param socket_default_value: Default value of the socket input widget.
        :type socket_default_value: Union[str, int, float, list]
        :param socket_str_type: Type the socket.
        :type socket_str_type: list
        """

        super().__init__(node, index, position, socket_color, multi_edges, count_on_this_node_side, is_input)

        self.socket_label: str = socket_label
        self.socket_input_index: int = socket_input_index
        self.socket_default_value: object = socket_default_value
        if socket_str_type is None:
            socket_str_type = ("*", )
        self.socket_str_type: tuple = socket_str_type
        self.grSocket.init_inner_widgets(self.socket_label, self.socket_input_index, self.socket_default_value)


class FCNNodeContentView(QDMNodeContentWidget):
    """The visual representation of the node content.

    The visual node content is composed by the labels and input widgets passed by the initialised input and output
    sockets. All widgets are arranged row wise by a QFormLayout and stored in class attributes. Labels and widgets of
    input sockets are stored in the input_labels and input_widgets lists and labels and widgets of output sockets are
    passed to the corresponding output_labels and output_widgets lists.

    Attributes:
        input_labels (list[QLabel]): Input labels of the input sockets.
        input_widgets (list[QWidget]): Input widgets of the input sockets.
        output_labels (list[QLabel]): Output labels of the output sockets.
        output_widgets (list[QWidget]): Output widgets of the output sockets.
        layout (QFormLayout): Layout of the node content widget.
    """

    input_widgets: list
    input_labels: list
    output_widgets: list
    output_labels: list
    layout: QFormLayout

    def initUI(self):
        """Initializes the node content ui layout.

       The initUI method initializes and sets the layout of the content widget as a QFormLayout. It is called by the
       contractor of the parent class QDMNodeContentWidget.
       """

        self.hide()  # Hack for recalculating content geometry before updating socket position.
        self.layout: QFormLayout = QFormLayout(self)
        self.layout.setObjectName(self.node.content_label_objname)
        self.setLayout(self.layout)

    def fill_content_layout(self):
        """Populates the content layout with socket labels and widgets.

        This method loops over all present input and output sockets af the parent node. Labels and input widgets are
        added to the QFormLayout and references to the widgets and labels are saved in the corresponding class attribute
        lists input_labels, input_widgets output_labels and output_widgets.

        Note:
            To query the individual sockets, they must already be initiated. For this reason the call of this method
            does not take place in the initUI method of this class, but in the constructor of the FCNNode class after
            initiation of the node with its sockets.
       """

        self.input_labels: list = []
        self.input_widgets: list = []
        self.output_labels: list = []
        self.output_widgets: list = []

        for socket in self.node.inputs:
            self.input_labels.append(socket.grSocket.label_widget)
            self.input_widgets.append(socket.grSocket.input_widget)
            self.layout.addRow(socket.grSocket.label_widget, socket.grSocket.input_widget)

        for socket in self.node.outputs:
            self.output_labels.append(socket.grSocket.input_widget)
            self.output_widgets.append(socket.grSocket.label_widget)
            self.layout.addRow(socket.grSocket.input_widget, socket.grSocket.label_widget)
        self.show()  # Hack for recalculating content geometry before updating socket position.

        # Levels heights of labels and widgets to prevent layout from jumping when individual widgets are shown/hidden.
        if self.node.auto_layout is True:
            # Hack: Not for nodes with manual layout management
            for idx, input_label in enumerate(self.input_labels):
                input_label.setFixedHeight(self.input_widgets[idx].height())

    def update_content_ui(self, sockets_input_data: list) -> None:
        """Updates the node content ui.

        The node content ui may have to adapt to the socket input data. The method update_content_ui contains the ui
        logic of the node content. It is called by the eval_primer method of the node after the collection of the
        socket inputs and before the calculation of the output values and allows the manipulation of the content widgets
        at runtime.

        Note:
            The general sockets_input_data list has the signature
            [[s0_e0, s0_e1, ..., s0_eN],
             [s1_e0, s1_e1, ..., s1_eN],
             ...,
             [sN_e0, sN_e1, ..., sN_eN]],
             where s stands for input socket and e for connected edge.

        :param sockets_input_data: Socket input data (signature see above).
        :type sockets_input_data: list
        """

        pass

    def serialize(self) -> OrderedDict:
        """Serialises the node content to human-readable json file.

        The serialise method adds the content (int, float, string, ...) of each socket widget to a dictionary and returns
        it. It is called by the serialise method of the parent node.

        :return: Serialised data as human-readable json file.
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
            elif isinstance(widget, QPlainTextEdit):
                res["widget" + str(idx)] = str(widget.toPlainText())
        return res

    def deserialize(self, data: dict, hashmap=None, restore_id: bool = True) -> bool:
        """Deserializes the node content.

        Deserialization method which takes data in dict format with helping hashmap containing references to existing
        entities.

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
                if not isinstance(widget, QLabel):
                    value: str = data["widget" + str(idx)]
                    if isinstance(widget, QLineEdit):
                        widget.setText(value)
                    elif isinstance(widget, QSlider):
                        widget.setValue(int(value))
                    elif isinstance(widget, QComboBox):
                        widget.setCurrentIndex(int(value))
                    elif isinstance(widget, QPlainTextEdit):
                        widget.setPlainText(value)
        except Exception as e:
            NodeException.nodesError("core",self.__class__.__name__,"deserialize","hidden")
            dumpException(e)
        return res


class FCNNodeView(QDMGraphicsNode):
    """Visual representation of a node in the node core scene.

    The visual node is a QGraphicsItem that is display in a QGraphicsScene instance. In addition, it serves as a
    container for the visual node content (see FCNNodeContentView class).The FCNNodeView class specifies all the
    necessary geometric information needed, to display a node in the scene.

    Attributes:
        width (int): Current width of the node.
        height (int): Current height of the node.
        collapsed_height (int): Height of the collapsed node.
        default_height (int): Default (uncollapsed) height of the node.
        edge_roundness (int): Roundness of the node corners.
        edge_padding (int): Padding between node and node content.
        title_horizontal_padding (int): Horizontal padding between node and node title.
        title_vertical_padding (int): Vertical padding between node and node title.
        icons (QImage): Status icons of the node, that is displayed in the top left corner.
    """

    width: int
    height: int
    collapsed_height: int
    default_height: int
    edge_roundness: int
    edge_padding: int
    title_horizontal_padding: int
    title_vertical_padding: int
    icons: QImage
    main_icon: QImage

    def initSizes(self):
        """Initialises the size of the visual node.

        This method sets the class attributes for the node dimensions and content paddings.
        """

        super().initSizes()
        self.width: int = 250
        self.height: int = 230
        self.default_height: int = self.height
        self.collapsed_height: int = 50
        self.edge_roundness: int = 6
        self.edge_padding: int = 10
        self.title_horizontal_padding: int = 12
        self.title_vertical_padding: int = 10

    def initAssets(self):
        """Initialises the status icons and the main icon of the node.

        Status icons indicate whether a node is valid, invalid or dirty. This method sets the class attribute for the
        status icons. The path to the main icon is defined by the icon class variable of the FCNNode class.
        """

        super().initAssets()
        path: str = locator.icon("nodes_status_icon.png")
        self.icons: QImage = QImage(path)
        self.main_icon: QImage = QImage(self.node.icon)

    def paint(self, painter, q_style_option_graphics_item, widget=None):
        """Paints the appropriate status icons on the visual node representation.

       Status icons indicate whether a node is valid, invalid or dirty. All status icons are in a single landscape
       image. A corresponding horizontal offset is used to select the required image section via translation. This
       method selects and draws the corresponding image section through the QPainter instance.
       """
        super().paint(painter, q_style_option_graphics_item, widget)

        painter.drawImage(QRectF(-12, -12, 24, 24), self.main_icon, QRectF(self.main_icon.rect()))
        status_icon_placement = QRectF(self.width-12, -12, 24.0, 24.0)
        if self.node.isDirty():
            painter.drawImage(status_icon_placement, self.icons, QRectF(0, 0, 24, 24))
        if self.node.isInvalid():
            painter.drawImage(status_icon_placement, self.icons, QRectF(48, 0, 24, 24))


class FCNNode(Node):
    """Data model class for a node in FreeCAD Nodes (fc_nodes).

     The FCNNode class contains the complete data model of a node. All necessary information is stored and managed
     either in class variables or attributes. This concerns not only the visual representation (ui) of the node in the
     node core scene including node content and sockets, but also the complete evaluation logic.

     General instance independent data is stored in class variables. These are:
     - icon (str): Path to the node image, displayed in the node list box (QListWidget).
     - op_code (int): Unique index of the node, used to register the node in the app, referring to nodes_conf.py.
     - op_title (str): Title of the node, display in the node header.
     - op_category (str): Node category used for structuring scenes context menu and node drop box.
     - content_label_objname (str): Label of the content widget, used by qss stylesheets.
     - GraphicsNode_class (QDMGraphicsNode): Name of node ui class.
     - NodeContent_class (QDMNodeContentWidget): Name of node content ui class.
     - Socket_class (Socket): Name of socket class.

     Attributes:
        input_init_list (list(tuple)): Definition of the input sockets with the signature [(socket_type (int),
            socket_label (str), socket_widget_index (int), widget_default_value (obj), multi_edge (bool))]
        outputs_init_list (list(tuples)): Definition of the output sockets with the signature [(socket_type (int),
            socket_label (str), socket_widget_index (int),widget_default_value (obj), multi_edge (bool))]
        content (FCNNodeContentView): Reference to the node content widget.
        sockets_input_data (list): Data structure that contains all input data either from widgets or other nodes with
            the signature [[s1], [s2], ..., [sn]].
        output_data_cache (list): Cache storage for the result of the node evaluation.
        input_socket_position (int): Initial position of the input sockets, referring to node_sockets.py.
        output_socket_position (int): Initial position of the output sockets, referring to node_sockets.py.
        socket_spacing (int): Vertical distance between individual socket circles.
        default_title (str): Stores the default title of the node for resetting purpose.

     Note:
        If input_socket_position is set to LEFT_BOTTOM and output_socket_position is set to RIGHT_BOTTOM,
        the socket positions are calculated by the content layout based on the input and output widgets of the sockets.
    """

    icon: str = ""
    op_code: int = -1
    op_title: str = ""
    op_category = "Default"
    content_label_objname: str = ""

    GraphicsNode_class: FCNNodeView = FCNNodeView
    NodeContent_class: QDMNodeContentWidget = FCNNodeContentView
    Socket_class: Socket = FCNSocket

    inputs_init_list: list
    output_init_list: list
    content: FCNNodeContentView
    sockets_input_data: list
    output_data_cache: list
    input_socket_position: int
    output_socket_position: int
    socket_spacing: int
    default_title: str

    def __init__(self, scene: Scene, inputs_init_list: list = None, outputs_init_list: list = None,
                 width: int = 250, auto_layout: bool = True):
        """Constructor of the FCNNode class.

        Note:
            Example inputs_init_list:
            inputs_init_list: list = [(0, "Format", 3, ["Value", "Percent"], True, ("int")),
                                      (0, "Min", 1, 0, True, ("int")), (0, "Max", 1, 100, True, ("int")),
                                      (0, "Val", 2, [0, 100, 50], True, ("int"))]

            Example outputs_init_list:
            outputs_init_list: list = [(0, "Range", 0, 0, True, ("int", "float")),
                                       (0, "Val", 0, 0, True, ("int", "float"))]

        :param scene: Editor Scene in which the node is to be inserted.
        :type scene: Scene
        :param inputs_init_list: Definition of the input sockets with the signature [(socket_type (int), socket_label
            (str), socket_widget_index (int), widget_default_value (obj), multi_edge (bool))]
        :type inputs_init_list: list
        :param outputs_init_list: Definition of the output sockets with the signature [(socket_type (int), socket_label
            (str), socket_widget_index (int), widget_default_value (obj), multi_edge (bool))]
        :type outputs_init_list: list
        :param width: Width of the node.
        :type width: int
        :param auto_layout: Is node height managed by Qt layout manager or manual?
        :type auto_layout: bool
        """
        
        self.inputs_init_list: list = inputs_init_list
        self.output_init_list: list = outputs_init_list
        self.auto_layout = auto_layout

        super().__init__(scene, self.__class__.op_title, self.inputs_init_list, self.output_init_list)
        self.default_title = self.title

        # Fill content after parent (and socket) initialisation, because the fill_content_layout method loops over all
        # sockets. Therefore, the sockets must already be present in the data model of the node.
        self.content.fill_content_layout()

        # Set node size and adjust content layout.
        height = (self.content.layout.totalMinimumSize().height() + self.grNode.title_height +
                  2*self.grNode.edge_padding)
        self.grNode.height = height
        self.grNode.default_height = height
        self.grNode.width = width
        self.content.setFixedHeight(self.grNode.height - self.grNode.title_vertical_padding -
                                    self.grNode.edge_padding - self.grNode.title_height)
        self.content.setFixedWidth(self.grNode.width - 2 * self.grNode.edge_padding)

        # Update socket position and spacing
        self.place_sockets()
        self.socket_spacing = 22

        # Initialise evaluation
        self.output_data_cache = list()  # Internal output_data cache
        self.markDirty()  # Set node flag to dirty
        self.eval()  # Start initial evaluation

    def update_content_status(self):
        """Updates the content input widget value and state.
        """

        for socket in self.inputs:
            socket.grSocket.update_widget_status()

    def place_sockets(self):
        """Updates the socket positions.

        Calls the setSocketPosition method of all sockets. It causes all sockets to re-fetch their position within
        the node using the getSocketPosition method of this class.
        """

        for socket in self.inputs:
            socket.setSocketPosition()
        for socket in self.outputs:
            socket.setSocketPosition()

    def collapse_node(self, collapse: bool = False) -> None:
        """Toggles node state between default and collapsed.

        Nodes can be collapsed to a smaller size to improve the clarity of a node graph. This function switches between
        the normal and collapsed node size, by showing or hiding the node content and adjusting the corresponding
        socket and edge positions.

        :param collapse: Shall the node collapse (True or False)?
        :type collapse: bool
        """

        if collapse is True:
            # Collapse node
            self.content.hide()
            self.grNode.height = self.grNode.collapsed_height

            self.socket_spacing = 10
            for socket in self.inputs:
                socket.position = LEFT_CENTER
            for socket in self.outputs:
                socket.position = RIGHT_CENTER

        else:
            # Reset node to uncollapsed
            self.content.show()
            self.grNode.height = self.grNode.default_height

            self.socket_spacing = 22
            for socket in self.inputs:
                socket.position = LEFT_BOTTOM
            for socket in self.outputs:
                socket.position = RIGHT_BOTTOM

        self.place_sockets()  # Update socket positions
        self.updateConnectedEdges()

    def getSocketPosition(self, index: int, position: int, num_out_of: int = 1) -> [int, int]:
        """Calculates the position of an individual socket within the node geometry.

        The node position is determined by the node content layout. Each socket is horizontally centered to its node
        label, that is arranged by the node content layout.

        :param index: Index of the target socket.
        :type index: int
        :param position: Position of the target socket, referring to node_sockets.py.
        :type position: int
        :param num_out_of: Total number of sockets on this position.
        :type num_out_of: int
        :return: Calculated position vector of the socket.
        :rtype: [int, int]
        """

        # Calculates default socket position
        x, y = super().getSocketPosition(index, position, num_out_of)

        if hasattr(self.content, "input_labels"):
            # If input labels have already been initiated, adjust the y coordinate according the label position.
            if position == LEFT_BOTTOM:
                elem: QWidget = self.content.input_labels[index]
                y = self.grNode.title_vertical_padding + self.grNode.title_height + elem.geometry().topLeft().y() + \
                    (elem.geometry().height() // 2)

            elif position == RIGHT_BOTTOM:
                elem: QWidget = self.content.output_labels[index]
                y = self.grNode.title_vertical_padding + self.grNode.title_height + elem.geometry().topLeft().y() + \
                    (elem.geometry().height() // 2)

            elif position in (LEFT_CENTER, RIGHT_CENTER):
                num_sockets = num_out_of
                node_height = self.grNode.height
                top_offset = self.grNode.title_vertical_padding
                available_height = node_height

                total_height_of_all_sockets = (num_sockets - 1) * self.socket_spacing + 6
                new_top = available_height - total_height_of_all_sockets
                y = new_top/2 + top_offset + index * self.socket_spacing

        return [x, y]

    def initSettings(self):
        """Initialises default socket position.

       The socket positions input_socket_position and output_socket_position are used, to calculate the default socket
       location and distribution within the node geometry.

       Note:
           If set to LEFT_BOTTOM and RIGHT_BOTTOM, the position of the socket input widgets within
           the content layout is used, to calculate the socket positions.
       """

        super().initSettings()
        self.input_socket_position: int = LEFT_BOTTOM
        self.output_socket_position: int = RIGHT_BOTTOM

    def initSockets(self, inputs: list, outputs: list, reset: bool = True):
        """Create the input and output sockets of the node.

        The initSockets method instantiates the socket data model classes, along with the corresponding socket ui
        classes. All necessary information for the individual sockets are passes through the inputs and outputs lists.

        :param inputs: Definition of the input sockets with the signature [(socket_type (int), socket_label (str),
            socket_widget_index (int), widget_default_value (obj), multi_edge (bool))]
        :type inputs: list(tuple)
        :param outputs: Definition of the output sockets with the signature [(socket_type (int), socket_label (str),
            socket_widget_index (int), widget_default_value (obj), multi_edge (bool))]
        :type outputs: list(tuple)
        :param reset: True destroys and removes old sockets.
        :type reset: bool
        """

        if reset:
            # Clear old sockets
            if hasattr(self, 'inputs') and hasattr(self, 'outputs'):
                # Remove visual sockets from scene
                for socket in (self.inputs + self.outputs):
                    self.scene.grScene.removeItem(socket.grSocket)
                self.inputs: list = []
                self.outputs: list = []

        # Create new sockets
        counter: int = 0
        for item in inputs:
            if len(item) > 5:
                socket_str_type = item[5]
            else:
                socket_str_type: tuple = ('*', )

            socket: FCNSocket = self.__class__.Socket_class(
                node=self, index=counter, position=self.input_socket_position,
                socket_color=item[0], multi_edges=item[4],
                count_on_this_node_side=len(inputs), is_input=True, socket_label=item[1], socket_input_index=item[2],
                socket_default_value=item[3], socket_str_type=socket_str_type
            )
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            if len(item) > 5:
                socket_str_type = item[5]
            else:
                socket_str_type: tuple = ('*', )

            socket: FCNSocket = self.__class__.Socket_class(
                node=self, index=counter, position=self.output_socket_position,
                socket_color=item[0], multi_edges=item[4],
                count_on_this_node_side=len(outputs), is_input=False, socket_label=item[1], socket_input_index=item[2],
                socket_default_value=item[3], socket_str_type=socket_str_type
            )
            counter += 1
            self.outputs.append(socket)

    def eval(self, index: int = 0) -> list:
        """Top level evaluation method of the node.

        A node evaluates the values for the output sockets based on the input socket values and the processing logic of
        the eval_primer and eval_operation methods. If a node is not dirty or invalid, the cached data is returned.
        Otherwise, a new calculation is delegated to the eval_primer method. The method calculates the data for all
        output sockets, but returns only the data of the requested (indexed) output.

        :param index: Index of the output socket data, that is returned.
        :type index: int
        :return: Result of the evaluation or the requested output.
        :rtype: list
        """

        if not self.isDirty() and not self.isInvalid():
            # Return cached result for the indexed (desired) output socket
            if DEBUG:
                print("_> returning cached %s output_data_cache:" % self.__class__.__name__, self.output_data_cache)
            return self.output_data_cache[index]
        try:
            # Run new evaluation and return the desired output socket (index)
            output_data: list = self.eval_primer()
            if output_data:
                return output_data[index]
        except (ValueError, TypeError, SyntaxError, NameError, ZeroDivisionError, IndexError, AttributeError) as e:
            NodeException.nodesWarning("core",self.__class__.__name__,"eval",str(e));
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantsDirty()
        except Exception as e:
            NodeException.nodesError("core",self.__class__.__name__,"eval",str(e));
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            dumpException(e)

    def eval_primer(self) -> list:
        """Prepares the evaluation of the output sockets.

        Input values are collected from connected nodes or socket input widgets, stored in the sockets_input_data list
        and passed to the eval_operation method. Before the calculation, the content ui is updated. Calculated results
        are stored in the output_data_cache.

        :return: Socket output data.
        :rtype: list
        """

        self.update_content_status()  # Update node content widgets

        if self.content.isHidden():
            # Hack: Updates the node title
            self.collapse_node(True)

        # Build input data structure
        self.sockets_input_data: list = []  # Container for input data
        for socket in self.inputs:
            socket_input_data: list = []
            if socket.hasAnyEdge():
                # From connected nodes
                for edge in socket.edges:
                    other_socket: Socket = edge.getOtherSocket(socket)
                    other_socket_node: Node = other_socket.node
                    other_socket_index: int = other_socket.index
                    other_socket_value_list: list = other_socket_node.eval(other_socket_index)
                    for other_socket_value in other_socket_value_list:
                        socket_input_data.append(other_socket_value)
            else:
                # From input widgets
                socket_input_widget: QWidget = socket.grSocket.input_widget
                if socket_input_widget is not None:
                    if isinstance(socket_input_widget, QLineEdit):
                        input_str: str = socket_input_widget.text()
                        try:
                            socket_input_data.append(float(input_str))
                        except ValueError as e:  # as e:
                            NodeException.nodesWarning("core",self.__class__.__name__,"eval_primer",str(e));
                            socket_input_data.append(input_str)

                    elif isinstance(socket_input_widget, QSlider):
                        input_value: int = socket_input_widget.value()
                        socket_input_data.append(input_value)

                    elif isinstance(socket_input_widget, QComboBox):
                        input_value: int = socket_input_widget.currentIndex()
                        socket_input_data.append(input_value)

                    elif isinstance(socket_input_widget, QPlainTextEdit):
                        input_value: str = socket_input_widget.toPlainText()
                        socket_input_data.append(input_value)

            self.sockets_input_data.append(socket_input_data)

        self.content.update_content_ui(self.sockets_input_data)  # Update node content ui
        sockets_output_data: list = self.eval_operation(self.sockets_input_data)  # Calculate socket output

        self.output_data_cache: list = sockets_output_data  # Cache calculation result
        self.markDirty(False)
        self.markInvalid(False)

        # self.format_tool_tip()
        self.grNode.setToolTip(str(self.output_data_cache))  # For better data structure debugging

        self.markDescendantsDirty()
        self.evalChildren()
        if DEBUG:
            print("%s::__eval()" % self.__class__.__name__, "self.output_data_cache = ", self.output_data_cache)
        return sockets_output_data

    def format_tool_tip(self):
        rich_text: str = ""
        for input_socket in self.inputs:
            rich_text += f"<b><i>{input_socket.socket_label}({','.join(input_socket.socket_str_type)})</i></b> "
        rich_text += "<br/>"
        for i, output_socket in enumerate(self.output_data_cache):
            rich_text += f"<b>{self.outputs[i].socket_label}({','.join(self.outputs[i].socket_str_type)}): </b>"
            for outLine in output_socket:
                rich_text += f"{outLine}<br/>"
        self.grNode.setToolTip(rich_text)

    def eval_operation(self, sockets_input_data: list) -> list:
        """Calculation of the socket outputs.

        The eval_operation is responsible or the actual calculation of the socket outputs. It processes the input data
        structure passed in through the method parameter socket_input_data and returns the calculation result as a list,
        with one sublist per output socket.

        Note:
            The general sockets_input_data list has the signature
            [[s0_e0, s0_e1, ..., s0_eN],
             [s1_e0, s1_e1, ..., s1_eN],
             ...,
             [sN_e0, sN_e1, ..., sN_eN]],
             where s stands for input socket and e for connected edge.

        :param sockets_input_data: Socket input data.
        :type sockets_input_data: list
        :return: Calculated output data as a list with one sublist per output socket.
        :rtype: list
        """

        # Default implementation
        return [[0], [0]]

    def onInputChanged(self, socket: Socket):
        """Callback method for input changed events.

        Each new data input (i.e. a text change in a socket input widget) requires a re-evaluation of the node, which is
        triggered by this method.

        :param socket: Socket trigger of the input change.
        :type socket: Socket
        """

        super().onInputChanged(socket)
        self.eval()
        if DEBUG:
            print("%s::__onInputChanged" % self.__class__.__name__, "self.output_data_cache = ", self.output_data_cache)

    def onDoubleClicked(self, event) -> None:
        """Callback method for double click events.

        A double click toggles the node size between default and collapsed size.

        :param event: Double click event triggered by the QGraphicsScene instance.
        :type event: QGraphicsSceneMouseEvent
        """

        if self.content.isHidden():
            self.collapse_node(False)
        else:
            self.collapse_node(True)

    def onDeserialized(self, data: dict):
        """Event manually called when this node was deserialized. Currently called when node is deserialized from scene
        Passing data containing the data which have been deserialized.
        """

        self.collapse_node(bool(data['is_collapsed']))

    def serialize(self) -> OrderedDict:
        """Serialises the node to human-readable json file.

        The serialise method adds the node date to a dictionary and returns it. It is called by the serialise method of
        the QGraphicsScene node_scene.Scene.serialize.

        :return: Serialised data as human-readable json file.
        :rtype: OrderedDict
        """

        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        res['is_collapsed'] = self.content.isHidden()
        return res

    def deserialize(self, data: dict, hashmap=None, restore_id: bool = True, *args, **kwargs) -> bool:
        """Deserializes the node.

        Deserialization method which takes data in dict format with helping hashmap containing references to existing
        entities.

        :param data: Dictionary containing serialized data.
        :type data: dict
        :param hashmap: Helper dictionary containing references (by id == key) to existing objects.
        :type hashmap: dict
        :param restore_id: True if we are creating new content. False is useful when loading existing content of which
            we want to keep the existing object's id.
        :type restore_id: bool
        :return: True if deserialization was successful, otherwise False.
        :rtype: bool
        """

        if hashmap is None:
            hashmap = {}
        res = super().deserialize(data, hashmap, restore_id)

        if DEBUG:
            print("Deserialized Node '%s'" % self.__class__.__name__, "res:", res)
        return res
