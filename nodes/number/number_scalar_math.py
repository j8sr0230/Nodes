# -*- coding: utf-8 -*-
###################################################################################
#
#  number_scalar_math.py
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

import awkward as ak
from qtpy.QtWidgets import QComboBox, QLayout, QVBoxLayout
from qtpy.QtCore import Qt

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel, FCNNodeView, FCNNodeContentView

from nodes_locator import icon


class ScalarMathInputContent(QDMNodeContentWidget):

    layout: QLayout
    edit: QComboBox

    def initUI(self):
        self.layout: QLayout = QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.layout)

        self.edit: QComboBox = QComboBox(self)
        self.edit.addItems(["a+b", "a-b", "a*b", "a/b", "a^b"])
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
class ScalarMath(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Scalar Math"
    op_category: str = "Number"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("", True), ("", True)],
                         outputs_init_list=[("", True)])

        self.grNode.resize(120, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def initInnerClasses(self):
        self.content: QDMNodeContentWidget = ScalarMathInputContent(self)
        self.grNode: QDMGraphicsNode = FCNNodeView(self)
        self.content.edit.currentIndexChanged.connect(self.onInputChanged)

    def eval_operation(self, sockets_input_data: list) -> list:
        op_code: int = self.content.edit.currentIndex()
        a_array = ak.Array(sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [0])
        b_array = ak.Array(sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [1])

        # Outputs
        if op_code == 0:  # Add
            res = a_array + b_array
        elif op_code == 1:  # Sub
            res = a_array - b_array
        elif op_code == 2:  # Mul
            res = a_array * b_array
        elif op_code == 3:  # Div
            res = a_array / b_array
        elif op_code == 4:  # Pow
            res = a_array ** b_array
        else:
            raise ValueError("Unknown operation (Op)")

        return [res.tolist()]
