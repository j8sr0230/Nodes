# -*- coding: utf-8 -*-
###################################################################################
#
#  fcn_default_node.py
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
"""Module for a default node in the FreeCAD Nodes application."""
from collections import OrderedDict
from typing import Optional

from qtpy.QtGui import QImage, QColor, QPen, QBrush, QFont
from qtpy.QtCore import QRectF, Qt

from nodeeditor.node_scene import Scene
from nodeeditor.node_node import Node
from nodeeditor.node_socket import Socket, LEFT_CENTER, RIGHT_CENTER
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_socket import QDMGraphicsSocket
from nodeeditor.utils import dumpException

import fcn_locator as locator


DEBUG = False


class FCNSocketView(QDMGraphicsSocket):
    """View provider for the FCNSocketModel class."""

    def paint(self, painter, option, widget=None):
        """Overwritten method of the class nodeeditor.node_graphics_socket.QDMGraphicsSocket."""

        super().paint(painter, option, widget)


class FCNSocketModel(Socket):
    """Model class for a node socket."""

    Socket_GR_Class = FCNSocketView

    socket_name: str

    def __init__(self, node: Node, index: int = 0, position: int = LEFT_CENTER, socket_color: int = 1,
                 multi_edges: bool = True, count_on_this_node_side: int = 1, is_input: bool = False,
                 socket_name: str = ""):
        """Overwritten constructor of the class nodeeditor.node_socket.Socket.

        :param socket_name: Socket name
        :type socket_name: str
        """

        super().__init__(node, index, position, socket_color, multi_edges, count_on_this_node_side, is_input)
        self.socket_name: str = socket_name


class FCNNodeContentView(QDMNodeContentWidget):
    def initUI(self):
        # lbl = QLabel("Hello World!", self)
        # lbl.setObjectName(self.node.content_label_objname)
        pass


class FCNNodeView(QDMGraphicsNode):
    """View provider for the FCNNodeModel class.

    Attributes:
        width (int): Width of the node
        height (int): Height of the node
        edge_roundness (int): Roundness of the node corners
        edge_padding (int): Padding between node and node content
        title_height (int) Height of the node title
        title_horizontal_padding (int): Horizontal padding between node and node title
        title_vertical_padding (int): Vertical padding between node and node title
        status_icons (QImage): Status icons of the node, that is displayed in the top left corner
    """

    width: int
    height: int
    edge_roundness: int
    edge_padding: int
    title_height: int
    title_horizontal_padding: int
    title_vertical_padding: int

    _title_color: QColor
    _title_font: QFont
    _color: QColor
    _color_selected: QColor
    _color_hovered: QColor
    _pen_default: QPen
    _pen_selected: QPen
    _pen_hovered: QPen
    _brush_title: QPen
    _brush_background: QBrush
    status_icons: QImage

    def initSizes(self):
        """Overwritten method of the class nodeeditor.node_graphics_node.QDMGraphicsNode."""

        self.width: int = 120
        self.height: int = 120
        self.edge_roundness: int = 10
        self.edge_padding: int = 10
        self.title_height: int = 30
        self.title_horizontal_padding: int = 4
        self.title_vertical_padding: int = 4

    def initAssets(self):
        """Overwritten method of the class nodeeditor.node_graphics_node.QDMGraphicsNode."""

        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 10)

        self._color = QColor("#7F000000")
        self._color_selected = QColor("#FFFFA637")
        self._color_hovered = QColor("#FF37A6FF")

        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(2.0)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(2.0)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(3.0)

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

        self.status_icons: QImage = QImage(locator.icon("fcn_status_icon.png"))

    def paint(self, painter, option, widget=None):
        """Overwritten method of the class nodeeditor.node_graphics_node.QDMGraphicsNode."""

        super().paint(painter, option, widget)

        status_icon_placement = QRectF(self.width-12, -12, 24, 24)
        if self.node.isDirty():
            painter.drawImage(status_icon_placement, self.status_icons, QRectF(0, 0, 24, 24))
        if self.node.isInvalid():
            painter.drawImage(status_icon_placement, self.status_icons, QRectF(48, 0, 24, 24))


class FCNNodeModel(Node):
    """Model class for a node in the FreeCAD Nodes application.

     Class variables:
     - icon (str): Path to the node icon image
     - op_code (int): Unique index of the node, used to register the node in the app
     - op_title (str): Title of the node
     - op_category (str): Node category
     - content_label_objname (str): Label of the content widget (qss identifier)
     - GraphicsNode_class (QDMGraphicsNode): Name of the view class o the node
     - NodeContent_class (QDMNodeContentWidget): Name of model class for the node content
     - Socket_class (Socket): Name of model class for the node sockets

     Attributes:
        input_init_list (list): Definition of the input sockets
        outputs_init_list (list): Definition of the output sockets
        content (QDMNodeContentWidget): Reference to the node content widget
        sockets_input_data (list): Data structure that contains all input data
        output_data_cache (list): Storage for the node evaluation result
        input_socket_position (int): Initial position of the input sockets
        output_socket_position (int): Initial position of the output sockets
    """

    icon: str = ""
    op_code: int = -1
    op_title: str = ""
    op_category = "Default"
    content_label_objname: str = ""
    GraphicsNode_class: QDMGraphicsNode = FCNNodeView
    NodeContent_class: QDMNodeContentWidget = FCNNodeContentView
    Socket_class: Socket = FCNSocketModel

    input_socket_position: int
    output_socket_position: int
    sockets_input_data: list
    output_data_cache: list

    def __init__(self, scene: Scene, inputs_init_list: list = None, outputs_init_list: list = None):
        """Overwritten constructor of the class nodeeditor.node_node.Node."""

        super().__init__(scene, self.__class__.op_title, inputs_init_list, outputs_init_list)

        self.output_data_cache = list()
        self.markDirty()
        self.eval()

    def initSettings(self):
        """Overwritten method of the class nodeeditor.node_node.Node."""

        super().initSettings()

        self.input_socket_position: int = LEFT_CENTER
        self.output_socket_position: int = RIGHT_CENTER

    def initSockets(self, inputs: list, outputs: list, reset: bool = True):
        """Overwritten method of the class nodeeditor.node_node.Node."""

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
            socket: FCNSocketModel = self.__class__.Socket_class(
                node=self, index=counter, position=self.input_socket_position, count_on_this_node_side=len(inputs),
                is_input=True, socket_color=item[0], socket_name=item[1], multi_edges=item[2])
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket: FCNSocketModel = self.__class__.Socket_class(
                node=self, index=counter, position=self.output_socket_position, count_on_this_node_side=len(outputs),
                is_input=False, socket_color=item[0], socket_name=item[1], multi_edges=item[2])
            counter += 1
            self.outputs.append(socket)

    def eval(self, index: int = 0) -> list:
        """Overwritten method of the class nodeeditor.node_node.Node."""

        if not self.isDirty() and not self.isInvalid():
            # Return cached result for the indexed (desired) output socket
            if DEBUG:
                print("_> returning cached %s output_data_cache:" % self.__class__.__name__, self.output_data_cache)
            return self.output_data_cache[index]
        try:
            # Run new evaluation and return the desired output socket (index)
            return self.eval_primer()[index]
        except (ValueError, TypeError, SyntaxError, NameError, ZeroDivisionError, IndexError, AttributeError) as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantsDirty()
        except Exception as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            dumpException(e)

    def eval_primer(self) -> list:
        """Prepares the evaluation of the output sockets

        Input values are collected from connected nodes, stored in the sockets_input_data list and passed to the
        eval_operation method. Calculated results are passed to the output_data_cache.

        :return: Socket output data
        :rtype: list
        """

        # Build input data structure
        self.sockets_input_data: list = []  # Container for input data

        for socket in self.inputs:
            socket_input_data: list = []
            if socket.hasAnyEdge():
                for edge in socket.edges:
                    other_socket: Socket = edge.getOtherSocket(socket)
                    other_socket_node: Node = other_socket.node
                    other_socket_index: int = other_socket.index
                    other_socket_value_list: list = other_socket_node.eval(other_socket_index)
                    for other_socket_value in other_socket_value_list:
                        socket_input_data.append(other_socket_value)
            self.sockets_input_data.append(socket_input_data)

        self.output_data_cache: list = self.eval_operation(self.sockets_input_data)  # Calculate socket output
        self.markDirty(False)
        self.markInvalid(False)
        self.grNode.setToolTip(str(self.output_data_cache))
        self.markDescendantsDirty()
        self.evalChildren()

        if DEBUG:
            print("%s::__eval()" % self.__class__.__name__, "self.output_data_cache = ", self.output_data_cache)
        return self.output_data_cache

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
        """Overwritten method of the class nodeeditor.node_node.Node."""

        super().onInputChanged(socket)
        self.eval()
        if DEBUG:
            print("%s::__onInputChanged" % self.__class__.__name__, "self.output_data_cache = ", self.output_data_cache)

    def onDoubleClicked(self, event) -> None:
        """Overwritten method of the class nodeeditor.node_node.Node."""

        super().onDoubleClicked(event)

    def serialize(self) -> OrderedDict:
        """Overwritten method of the class nodeeditor.node_node.Node."""

        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data: dict, hashmap=None, restore_id: bool = True, *args, **kwargs) -> bool:
        """Overwritten method of the class nodeeditor.node_node.Node."""

        if hashmap is None:
            hashmap = {}
        res = super().deserialize(data, hashmap, restore_id)

        if DEBUG:
            print("Deserialized Node '%s'" % self.__class__.__name__, "res:", res)
        return res
