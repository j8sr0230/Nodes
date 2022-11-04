# -*- coding: utf-8 -*-
###################################################################################
#
#  number_number_slider.py
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

from qtpy.QtWidgets import QSlider, QLineEdit, QLayout, QHBoxLayout
from qtpy.QtCore import Qt

from nodeeditor.node_content_widget import QDMNodeContentWidget

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel, FCNNodeView, FCNNodeContentView

from nodes_locator import icon


class SliderInputContent(QDMNodeContentWidget):

    layout: QLayout
    slider_edit: QSlider
    min_edit: QLineEdit
    max_edit: QLineEdit

    def initUI(self):
        self.layout: QLayout = QHBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.layout)

        self.min_edit: QLineEdit = QLineEdit("Min", self)
        self.min_edit.setAlignment(Qt.AlignLeft)
        self.min_edit.setObjectName(self.node.content_label_objname)

        self.slider_edit: QSlider = QSlider(Qt.Horizontal, self)
        self.slider_edit.setMinimum(0)
        self.slider_edit.setMaximum(100)
        self.slider_edit.setValue(50)
        self.slider_edit.setObjectName(self.node.content_label_objname)

        self.max_edit: QLineEdit = QLineEdit("Max", self)
        self.max_edit.setAlignment(Qt.AlignRight)
        self.max_edit.setObjectName(self.node.content_label_objname)

        self.layout.addWidget(self.min_edit)
        self.layout.addWidget(self.slider_edit)
        self.layout.addWidget(self.max_edit)

        self.min_edit.setMinimumWidth(30)
        self.max_edit.setMinimumWidth(30)
        self.layout.setStretchFactor(self.min_edit, 1)
        self.layout.setStretchFactor(self.slider_edit, 10)
        self.layout.setStretchFactor(self.max_edit, 1)

    def set_slider_min(self, min_value: str) -> bool:
        try:
            self.slider_edit.setMinimum(int(min_value))
            return True
        except ValueError:
            return False

    def set_slider_max(self, max_value: str) -> bool:
        try:
            self.slider_edit.setMaximum(int(max_value))
            return True
        except ValueError:
            return False

    def serialize(self) -> OrderedDict:
        res: OrderedDict = super().serialize()
        res['value'] = self.slider_edit.value()
        res['min'] = self.slider_edit.minimum()
        res['max'] = self.slider_edit.maximum()
        return res

    def deserialize(self, data: dict, hashmap=None, restore_id: bool = True) -> bool:
        if hashmap is None:
            hashmap = {}

        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.slider_edit.setValue(value)
            sld_min = data['min']
            self.slider_edit.setMinimum(sld_min)
            self.min_edit.setText(str(sld_min))
            sld_max = data['max']
            self.slider_edit.setMaximum(sld_max)
            self.max_edit.setText(str(sld_max))
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node
class NumberSlider(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Number Slider"
    op_category: str = "Number"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene, inputs_init_list=[], outputs_init_list=[("", True)])

        self.grNode.resize(250, 70)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def initInnerClasses(self):
        self.content: QDMNodeContentWidget = SliderInputContent(self)
        self.grNode: QDMGraphicsNode = FCNNodeView(self)

        self.content.min_edit.textChanged.connect(self.content.set_slider_min)
        self.content.max_edit.textChanged.connect(self.content.set_slider_max)
        self.content.slider_edit.valueChanged.connect(self.onInputChanged)

    def eval_operation(self, sockets_input_data: list) -> list:
        in_val: float = float(self.content.slider_edit.value())
        return [[in_val]]
