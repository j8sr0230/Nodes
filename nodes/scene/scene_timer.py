# -*- coding: utf-8 -*-
###################################################################################
#
#  scene_timer.py
#
#  Copyright (c) 2022 Florian Foinant-Willig <ffw@2f2v.fr>
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

from qtpy.QtWidgets import QLineEdit, QCheckBox, QLayout, QHBoxLayout
from qtpy.QtCore import Qt, QTimer
from nodeeditor.node_content_widget import QDMNodeContentWidget

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel, FCNNodeView, FCNNodeContentView
from nodes_locator import icon


DEBUG = False


class TimerInputContent(QDMNodeContentWidget):

    layout: QLayout
    interval_edit: QLineEdit
    run_checkbox: QCheckBox

    def initUI(self):
        self.layout: QLayout = QHBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.layout)

        self.interval_edit: QLineEdit = QLineEdit("1000", self)
        self.layout.addWidget(self.interval_edit)

        self.run_checkbox: QCheckBox = QCheckBox(self)
        self.layout.addWidget(self.run_checkbox)

        self.setObjectName(self.node.content_label_objname)

    def serialize(self) -> OrderedDict:
        res: OrderedDict = super().serialize()
        res['value'] = self.interval_edit.text()
        res['state'] = self.run_checkbox.isChecked()
        return res

    def deserialize(self, data: dict, hashmap=None, restore_id: bool = True) -> bool:
        if hashmap is None:
            hashmap = {}

        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.interval_edit.setText(value)
            state = data['state']
            self.run_checkbox.setChecked(state)

            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node
class Timer(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Timer"
    op_category: str = "Scene"
    content_label_objname: str = "fcn_node_bg"

    timer: QTimer

    def __init__(self, scene):
        super().__init__(scene=scene, inputs_init_list=[], outputs_init_list=[("", True)])

        self.grNode.resize(120, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def initInnerClasses(self):
        self.content: QDMNodeContentWidget = TimerInputContent(self)
        self.grNode: QDMGraphicsNode = FCNNodeView(self)
        self.content.interval_edit.textChanged.connect(self.onInputChanged)
        self.content.run_checkbox.stateChanged.connect(self.onInputChanged)

    def timer_callback(self):
        self.markInvalid()
        self.eval()

    def remove(self):
        super().remove()
        self.timer.stop()

    def eval_operation(self, sockets_input_data: list) -> list:
        op_code: bool = self.content.run_checkbox.isChecked()
        period: int = int(self.content.interval_edit.text())

        self.timer = QTimer()
        self.timer.start(period)
        self.timer.timeout.connect(self.timer_callback)

        if not op_code:
            self.timer.stop()
        else:
            self.timer.start()

        if DEBUG:
            print("Running timer no.:", self.timer.timerId())

        return [[self.timer.timerId()]]
