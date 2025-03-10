# -*- coding: utf-8 -*-
###################################################################################
#
#  nodes_default_node.py
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
"""Module containing a default node in the FreeCAD Nodes application."""
from collections import OrderedDict
from typing import Optional

from qtpy.QtGui import QImage, QColor, QPen, QBrush, QFont, QFontMetrics
from qtpy.QtWidgets import QGraphicsTextItem
from qtpy.QtCore import QRectF, Qt

import Exceptions as NodeExceptions;
from nodeeditor.node_scene import Scene
from nodeeditor.node_node import Node
from nodeeditor.node_socket import Socket, LEFT_CENTER, RIGHT_CENTER
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_socket import QDMGraphicsSocket
from nodeeditor.utils import dumpException

from Part import OCCError

import nodes_locator as locator


DEBUG = False


class FCNSocketView(QDMGraphicsSocket):
    """View provider for FCNSocketModel.

    Attributes:
        _color_label (QColor): Label color
        _pen_label (QPen): Label pen
    """

    _color_label: QColor
    _pen_label: QPen

    def initAssets(self):
        """Overwritten from nodeeditor.node_graphics_socket.QDMGraphicsSocket."""
        super().initAssets()

        self._color_label = QColor("#fff")
        self._pen_label = QPen(self._color_label)

    def paint(self, painter, option, widget=None):
        """Overwritten from nodeeditor.node_graphics_socket.QDMGraphicsSocket."""

        super().paint(painter, option, widget)

        painter.setPen(self._color_label)
        fm: QFontMetrics = QFontMetrics(painter.font())
        label_width: int = fm.width(self.socket.socket_label)
        font_height: int = fm.height()
        y: int = (-font_height // 2) - 1

        if self.socket.is_input:
            painter.drawText(self.radius + 5, y, label_width, font_height,
                             Qt.AlignVCenter, self.socket.socket_label)
        else:
            painter.drawText(-self.radius - label_width - 5, y, label_width, font_height,
                             Qt.AlignRight | Qt.AlignVCenter, self.socket.socket_label)


class FCNSocketModel(Socket):
    """Model class for a node socket."""

    Socket_GR_Class = FCNSocketView

    socket_label: str

    def __init__(self, node: Node, index: int = 0, position: int = LEFT_CENTER, socket_color: int = 1,
                 multi_edges: bool = True, count_on_this_node_side: int = 1, is_input: bool = False,
                 socket_label: str = ""):
        """Overwritten from nodeeditor.node_socket.Socket.

        :param socket_name: Socket label
        :type socket_name: str
        """

        super().__init__(node, index, position, socket_color, multi_edges, count_on_this_node_side, is_input)
        self.socket_label: str = socket_label


class FCNNodeContentView(QDMNodeContentWidget):
    """View provider (node content widget) for the node content."""

    def initUI(self):
        """Overwritten from nodeeditor.node_content_widget.QDMNodeContentWidget."""

        self.setStyleSheet("background:transparent;")


class FCNNodeView(QDMGraphicsNode):
    """View provider for FCNNodeModel.

    Attributes:
        width (int): Width of the node
        height (int): Height of the node
        edge_roundness (int): Roundness of the node corners
        edge_padding (int): Padding between node and node content
        title_height (int) Height of the node title
        title_horizontal_padding (int): Horizontal padding between node and node title
        title_vertical_padding (int): Vertical padding between node and node title
        status_icons (QImage): Status icons of the node (top right corner)
    """

    width: int
    height: int
    edge_roundness: int
    edge_padding: int
    title_height: int
    title_horizontal_padding: int
    title_vertical_padding: int
    status_icons: QImage

    def initSizes(self):
        """Overwritten from nodeeditor.node_graphics_node.QDMGraphicsNode."""

        self.width: int = 80
        self.height: int = 70
        self.edge_roundness: int = 3
        self.edge_padding: int = 5
        self.title_height: int = 28
        self.title_horizontal_padding: int = 5
        self.title_vertical_padding: int = 0

    def initAssets(self):
        """Overwritten from nodeeditor.node_graphics_node.QDMGraphicsNode."""

        super().initAssets()

        self.status_icons: QImage = QImage(locator.icon("nodes_status_icon.png"))

    def resize(self, width: int, height: int) -> None:
        """Resizes the visual node representation.

        :param width: New node width
        :type width: int
        :param height: New node height
        :type height: int
        """

        self.width: int = width
        self.height: int = height
        self.title_item.setTextWidth(self.width - 2 * self.title_horizontal_padding)
        self.grContent.setGeometry(QRectF(self.edge_padding, self.title_height + self.edge_padding,
                                          self.width - 2 * self.edge_padding,
                                          self.height - 2 * self.edge_padding - self.title_height))

    def paint(self, painter, option, widget=None):
        """Overwritten from nodeeditor.node_graphics_node.QDMGraphicsNode."""

        super().paint(painter, option, widget)

        status_icon_placement = QRectF(self.width-10, -10, 20, 20)
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
        input_socket_position (int): Initial position of the input sockets
        output_socket_position (int): Initial position of the output sockets
        inputs (list): List of input sockets
        outputs (list): List of output sockets
        sockets_input_data (list): Data structure that contains all input data
        output_data_cache (list): Storage for the node evaluation result
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
    inputs: list
    outputs: list
    sockets_input_data: list
    output_data_cache: list

    def __init__(self, scene: Scene, inputs_init_list: list = None, outputs_init_list: list = None):
        """Overwritten from class nodeeditor.node_node.Node."""

        super().__init__(scene, self.__class__.op_title, inputs_init_list, outputs_init_list)

        self.output_data_cache = list()
        self.markDirty()
        self.eval()

    def initSettings(self):
        """Overwritten from class nodeeditor.node_node.Node."""

        super().initSettings()

        self.input_socket_position: int = LEFT_CENTER
        self.output_socket_position: int = RIGHT_CENTER

    def initSockets(self, inputs: list, outputs: list, reset: bool = True):
        """Overwritten from class nodeeditor.node_node.Node."""

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
                is_input=True, socket_color=6, socket_label=item[0], multi_edges=item[1])
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket: FCNSocketModel = self.__class__.Socket_class(
                node=self, index=counter, position=self.output_socket_position, count_on_this_node_side=len(outputs),
                is_input=False, socket_color=6, socket_label=item[0], multi_edges=item[1])
            counter += 1
            self.outputs.append(socket)

    def getSocketPosition(self, index: int, position: int, num_out_of: int = 1) -> list:
        """Overwritten from class nodeeditor.node_node.Node."""

        x = self.socket_offsets[position] if position is LEFT_CENTER \
            else self.grNode.width + self.socket_offsets[position]

        y = 0
        if position in (LEFT_CENTER, RIGHT_CENTER):
            num_sockets = num_out_of
            node_height = self.grNode.height
            top_offset = self.grNode.title_height + self.grNode.edge_padding
            available_height = node_height - top_offset - self.grNode.edge_padding
            total_height_of_all_sockets = (num_sockets-1) * self.socket_spacing
            new_top = (available_height - total_height_of_all_sockets) // 2

            y = top_offset + new_top + index*self.socket_spacing + 1

        return [x, y]

    def eval(self, index: int = 0) -> list:
        """Overwritten from class nodeeditor.node_node.Node."""

        if not self.isDirty() and not self.isInvalid():
            # Return cached result for the indexed (desired) output socket
            if DEBUG:
                print("_> returning cached %s output_data_cache:" % self.__class__.__name__, self.output_data_cache)
            return self.output_data_cache[index]
        try:
            # Run new evaluation and return the desired output socket (index)
            return self.eval_primer()[index]
        except (ValueError, TypeError, SyntaxError, NameError, ZeroDivisionError, IndexError, AttributeError,
                OCCError, RuntimeError) as e:
            NodeExceptions.nodesWarning("Nodes","core",self.__class__.__name__,"eval",str(e));
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantsDirty()
        except Exception as e:
            NodeExceptions.nodesWarning("Nodes","core",self.__class__.__name__,"eval",str(e));
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
        self.grNode.setToolTip(str(self.output_data_cache))

        self.markDirty(False)
        self.markInvalid(False)
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

        :param sockets_input_data: Socket input data
        :type sockets_input_data: list
        :return: Calculated output data as a list with one sublist per output socket
        :rtype: list
        """

        # Default implementation
        return [[0]]

    def onInputChanged(self, socket: Socket):
        """Overwritten from nodeeditor.node_node.Node."""

        super().onInputChanged(socket)

        self.eval()
        if DEBUG:
            print("%s::__onInputChanged" % self.__class__.__name__, "self.output_data_cache = ", self.output_data_cache)

    def onDoubleClicked(self, event) -> None:
        """Overwritten from nodeeditor.node_node.Node."""

        super().onDoubleClicked(event)

    def serialize(self) -> OrderedDict:
        """Overwritten from nodeeditor.node_node.Node."""

        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data: dict, hashmap=None, restore_id: bool = True, *args, **kwargs) -> bool:
        """Overwritten from nodeeditor.node_node.Node."""

        if hashmap is None:
            hashmap = {}
        res = super().deserialize(data, hashmap, restore_id)

        if DEBUG:
            print("Deserialized Node '%s'" % self.__class__.__name__, "res:", res)
        return res
