# -*- coding: utf-8 -*-
###################################################################################
#
#  curves_arc_deg.py
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
class ArcDeg(FCNNodeModel):

    icon: str = icon("nodes_arc.svg")
    op_title: str = "Arc (Deg)"
    op_category: str = "Curves"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Radius", True), ("Point", True), ("Direction", True),
                                           ("Angle 1", True), ("Angle 2", True)],
                         outputs_init_list=[("Shape", True)])

        self.grNode.resize(120, 150)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def make_arc(parameter_zip: tuple) -> Part.Shape:
        radius = parameter_zip[0]
        position = parameter_zip[1]
        direction = parameter_zip[2]
        start_angel = parameter_zip[3]
        end_angle = parameter_zip[4]

        return Part.makeCircle(radius, position, direction, start_angel, end_angle)

    def eval_operation(self, sockets_input_data: list) -> list:
        # Get socket inputs
        radius_input: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [10]
        position_input: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [Vector(0, 0, 0)]
        direction_input: list = sockets_input_data[2] if len(sockets_input_data[2]) > 0 else [Vector(0, 0, 1)]
        start_angle_input: list = sockets_input_data[3] if len(sockets_input_data[3]) > 0 else [0]
        end_angle_input: list = sockets_input_data[4] if len(sockets_input_data[4]) > 0 else [360]

        # Broadcast and calculate result
        data_tree = broadcast_data_tree(radius_input, position_input, direction_input, start_angle_input,
                                        end_angle_input)
        arcs: list = list(map_objects(data_tree, tuple, self.make_arc))

        return [arcs]
