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
from qtpy import QtCore

from fcn_conf import register_node
from fcn_base_node import FCNNode
import fcn_locator as locator


DEBUG = True


@register_node
class Timer(FCNNode):

    icon: str = locator.icon("fcn_default.png")
    op_title: str = "Timer"
    op_category: str = "Scene"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        inputs: list = [(0, "p [ms]", 1, 1000, True)]
        outputs: list = [(0, "p [ms]", 0, 0, True)]
        width: int = 150

        self.timer = QtCore.QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.timer_callback)

        super().__init__(scene=scene, inputs_init_list=inputs, outputs_init_list=outputs, width=width)

    def timer_callback(self):
        self.markInvalid()
        self.eval()

    def remove(self):
        super().remove()

        if self.timer.isActive():
            self.timer.stop()

    def eval_operation(self, sockets_input_data: list) -> list:
        period: float = float(sockets_input_data[0][0])
        if self.timer.interval != period:
            self.timer.setInterval(period)

        if not self.timer.isActive():
            self.timer.start()

        if DEBUG:
            print("Tick")

        return [[period]]
