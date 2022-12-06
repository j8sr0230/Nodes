# -*- coding: utf-8 -*-
###################################################################################
#
#  surfaces_evaluate_srf.py
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
from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import map_objects, broadcast_data_tree

from nodes_locator import icon


@register_node
class EvaluateSurface(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Evaluate Srf"
    op_category: str = "Surfaces"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("U", True), ("V", True), ("Srf", True), ],
                         outputs_init_list=[("Point", True), ("Normal", True)])

        self.grNode.resize(120, 100)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def evaluate_surface(parameter_zip: tuple) -> tuple:
        u: float = parameter_zip[0]
        v: float = parameter_zip[1]
        surface: Part.Face = parameter_zip[2]

        return surface.valueAt(u, v), surface.normalAt(u, v)

    def eval_operation(self, sockets_input_data: list) -> list:
        # Get socket inputs
        u_input: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [0.0]
        v_input: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [0.0]
        surface_input: list = sockets_input_data[2]

        # Broadcast and calculate result
        data_tree: list = list(broadcast_data_tree(u_input, v_input, surface_input))
        result: list = list(map_objects(data_tree, tuple, self.evaluate_surface))

        # Distribute result to socket outputs
        position_output: list = list(map_objects(result, tuple, lambda pos_norm_tuple: pos_norm_tuple[0]))
        normal_output: list = list(map_objects(result, tuple, lambda pos_norm_tuple: pos_norm_tuple[1]))
        return [position_output, normal_output]

