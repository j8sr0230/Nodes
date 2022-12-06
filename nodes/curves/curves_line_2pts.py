# -*- coding: utf-8 -*-
###################################################################################
#
#  curves_line_2pts.py
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
class Line2Pts(FCNNodeModel):

    icon: str = icon("nodes_line.svg")
    op_title: str = "Line (2 Pts)"
    op_category: str = "Curves"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Point 1", True), ("Point 2", True)],
                         outputs_init_list=[("Shape", True)])

        self.grNode.resize(110, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def make_line(parameter_zip: tuple) -> Part.Shape:
        start: Vector = parameter_zip[0]
        end: Vector = parameter_zip[1]

        return Part.makeLine(start, end)

    def eval_operation(self, sockets_input_data: list) -> list:
        # Get socket inputs
        start_input: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [Vector(0, 0, 0)]
        end_input: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [Vector(10, 0, 0)]

        # Broadcast and calculate result
        data_tree: list = list(broadcast_data_tree(start_input, end_input))
        lines: list = list(map_objects(data_tree, tuple, self.make_line))

        return [lines]
