# -*- coding: utf-8 -*-
###################################################################################
#
#  clock_node.py
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
from fcn_conf import register_node
from fcn_base_node import FCNNode

import fcn_locator as locator

from PySide2 import QtCore

@register_node
class ClockNode(FCNNode):

    icon: str = locator.icon("fcn_default.png")
    op_title: str = "Clock"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene: 'Scene'):
        inputs: list = [(0, "period (s.)", 1, "0.1", True)]
        outputs: list = [(0, "tick", 0, 0, True)]
        width: int = 150

        self.timer = QtCore.QTimer()
        self.timer.start(100)
        self.timer.timeout.connect(self.timer_callback)

        super().__init__(scene=scene, inputs_init_list=inputs, outputs_init_list=outputs, width=width)

    def timer_callback(self):
        self.markInvalid()
        self.eval()

    def eval_operation(self, sockets_input_data: list) -> list:
        period: float = float(sockets_input_data[0][0]) * 1000
        if (self.timer.interval != period):
            self.timer.setInterval(period)
        return [[1]]
