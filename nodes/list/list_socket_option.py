# -*- coding: utf-8 -*-
###################################################################################
#
#  list_reshape.py
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
from collections import OrderedDict

from qtpy.QtWidgets import QComboBox, QLayout, QVBoxLayout
from qtpy.QtCore import Qt

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel, FCNNodeContentView
from core.nodes_default_node import FCNNodeView
from core.nodes_utils import flatten, simplify, graft, graft_topology, unwrap, wrap

from nodes_locator import icon


class SocketOpInputContent(QDMNodeContentWidget):

    layout: QLayout
    edit: QComboBox

    def initUI(self):
        self.layout: QLayout = QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.layout)

        self.edit: QComboBox = QComboBox(self)
        self.edit.addItems(['Flatten', 'Simplify', 'Graft', 'Graft Topology', 'Unwrap', 'Wrap'])
        self.edit.setObjectName(self.node.content_label_objname)

        self.layout.addWidget(self.edit)

    def serialize(self) -> OrderedDict:
        res: OrderedDict = super().serialize()
        res['value'] = str(self.edit.currentIndex())
        return res

    def deserialize(self, data: dict, hashmap=None, restore_id: bool = True) -> bool:
        if hashmap is None:
            hashmap = {}

        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setCurrentIndex(int(value))
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node
class SocketOption(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Socket Option"
    op_category: str = "List"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene, inputs_init_list=[("", True)], outputs_init_list=[("", True)])

        self.grNode.resize(140, 70)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def initInnerClasses(self):
        self.content: QDMNodeContentWidget = SocketOpInputContent(self)
        self.grNode: QDMGraphicsNode = FCNNodeView(self)
        self.content.edit.currentIndexChanged.connect(self.onInputChanged)

    def eval_operation(self, sockets_input_data: list) -> list:
        op_code: int = self.content.edit.currentIndex()
        in_array = sockets_input_data[0]

        # Outputs
        if op_code == 0:  # Flatten
            res = flatten(in_array)
        elif op_code == 1:  # Simplify
            res = simplify(in_array)
        elif op_code == 2:  # Graft
            res = graft(in_array)
        elif op_code == 3:  # Graft Topology
            res = graft_topology(in_array)
        elif op_code == 4:  # Unwrap
            res = unwrap(in_array)
        elif op_code == 5:  # Wrap
            res = wrap(in_array)
        else:
            raise ValueError("Unknown operation (Op)")
        return [res]
