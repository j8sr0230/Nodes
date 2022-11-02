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

from editor.nodes_conf import register_node
from editor.nodes_base_node import FCNNode
import nodes_locator as locator


DEBUG = False


@register_node
class Timer(FCNNode):

    icon: str = locator.icon("nodes_default.png")
    op_title: str = "Timer"
    op_category: str = "Scene"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        inputs: list = [(0, 'State', 3, ['Hold', 'Run'], False, ('int', )),
                        (0, "Period", 1, 1000, False, ('int', 'float'))]
        outputs: list = [(0, "Tick", 0, 0, True, ('int', 'float'))]
        width: int = 150

        self.timer = QtCore.QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.timer_callback)

        super().__init__(scene=scene, inputs_init_list=inputs, outputs_init_list=outputs, width=width)

    def timer_callback(self):
        try:
            self.markInvalid()
            self.eval()
        except AttributeError as e:
            if DEBUG:
                print(e)

    def remove(self):
        super().remove()
        self.timer.stop()

    def eval_operation(self, sockets_input_data: list) -> list:
        op_code: int = sockets_input_data[0][0]
        period: float = float(sockets_input_data[1][0])

        if self.timer.interval != period:
            self.timer.setInterval(period)

        if op_code == 0:  # Hold
            self.timer.stop()
        elif op_code == 1:  # Run
            self.timer.start()

        if DEBUG:
            print("Running timer no.:", self.timer.timerId())

        return [[period]]
