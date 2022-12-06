# -*- coding: utf-8 -*-
###################################################################################
#
#  number_number_range.py
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
import numpy as np

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import map_objects, broadcast_data_tree

from nodes_locator import icon


@register_node
class NumberRange(FCNNodeModel):

    icon: str = icon("nodes_number_range.svg")
    op_title: str = "Number Range"
    op_category: str = "Number"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Start", True), ("Stop", True), ("Step", True)],
                         outputs_init_list=[("Out", True)])

        self.grNode.resize(130, 100)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def make_range(parameter_zip: tuple) -> list:
        start: float = parameter_zip[0]
        stop: float = parameter_zip[1]
        step: float = parameter_zip[2]

        return list(np.arange(start, stop, step))

    def eval_operation(self, sockets_input_data: list) -> list:
        # Get socket inputs
        start_input = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [0.0]
        stop_input = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [10.0]
        step_input = sockets_input_data[2] if len(sockets_input_data[2]) > 0 else [1.0]

        # Broadcast and calculate result
        data_tree: list = list(broadcast_data_tree(start_input, stop_input, step_input))
        ranges: list = list(map_objects(data_tree, tuple, self.make_range))

        return [ranges]
