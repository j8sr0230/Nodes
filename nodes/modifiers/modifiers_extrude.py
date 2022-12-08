# -*- coding: utf-8 -*-
###################################################################################
#
#  modifiers_extrude.py
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
from FreeCAD import Vector
import Part

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import map_objects, broadcast_data_tree

from nodes_locator import icon


@register_node
class Extrude(FCNNodeModel):

    icon: str = icon("nodes_extrude.svg")
    op_title: str = "Extrude"
    op_category: str = "Modifiers"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Shape", True), ("Direction", True)],
                         outputs_init_list=[("Shape", True)])

        self.grNode.resize(120, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def make_extrusion(parameter_zip: tuple) -> Part.Shape:
        shape: Part.Shape = parameter_zip[0]
        direction: Vector = parameter_zip[1]

        return shape.extrude(direction)

    def eval_operation(self, sockets_input_data: list) -> list:
        # Get socket inputs
        shape_input: list = sockets_input_data[0]
        direction_input: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [Vector(0, 0, 1)]

        # Broadcast and calculate result
        data_tree: list = list(broadcast_data_tree(shape_input, direction_input))
        shapes: list = list(map_objects(data_tree, tuple, self.make_extrusion))

        return [shapes]
