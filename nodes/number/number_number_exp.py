# -*- coding: utf-8 -*-
###################################################################################
#
#  number_number_exp_op.py
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

from qtpy.QtWidgets import QLineEdit, QLayout, QVBoxLayout
from qtpy.QtCore import Qt

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel, FCNNodeContentView
from core.nodes_default_node import FCNNodeView

from nodes_locator import icon


class LineInputContent(QDMNodeContentWidget):

    layout: QLayout
    edit: QLineEdit

    def initUI(self):
        self.layout: QLayout = QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.layout)

        self.edit: QLineEdit = QLineEdit("1", self)
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)

        self.layout.addWidget(self.edit)

    def serialize(self) -> OrderedDict:
        res: OrderedDict = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data: dict, hashmap=None, restore_id: bool = True) -> bool:
        if hashmap is None:
            hashmap = {}

        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node
class NumberExp(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Number (exp.)"
    op_category: str = "Number"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene, inputs_init_list=[], outputs_init_list=[("", True)])

        self.grNode.resize(130, 70)
        self.grNode.initContent()
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def initInnerClasses(self):
        self.content: QDMNodeContentWidget = LineInputContent(self)
        self.grNode: QDMGraphicsNode = FCNNodeView(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

    def eval_operation(self, sockets_input_data: list) -> list:
        in_val: float = float(self.content.edit.text())
        return [[in_val]]
