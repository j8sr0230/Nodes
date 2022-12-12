# -*- coding: utf-8 -*-
###################################################################################
#
#  generators_solid_torus.py
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
class SolidBox(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Torus"
    op_category: str = "Generators"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Radius 1", True,), ("Radius 2", True), ("Point", True), ("Dir", True),
                                           ("V1 Angle", True), ("V2 Angle", True), ("U Angle", True)],
                         outputs_init_list=[("Shape", True)])

        self.grNode.resize(120, 190)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def make_torus(parameter_zip: tuple) -> Part.Shape:
        radius_1: float = parameter_zip[0]
        radius_2: float = parameter_zip[1]
        position: Vector = parameter_zip[2]
        direction: Vector = parameter_zip[3]
        v_1_angle: float = parameter_zip[4]
        v_2_angle: float = parameter_zip[5]
        u_angle: float = parameter_zip[6]

        return Part.makeTorus(radius_1, radius_2, position, direction, v_1_angle, v_2_angle, u_angle)

    def eval_operation(self, sockets_input_data: list) -> list:
        # Get socket inputs
        radius_1_input: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [50.0]
        radius_2_input: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [10.0]
        point_input: list = sockets_input_data[2] if len(sockets_input_data[2]) > 0 else [Vector(0, 0, 0)]
        dir_input: list = sockets_input_data[3] if len(sockets_input_data[3]) > 0 else [Vector(0, 0, 1)]
        v_1_angle_input: list = sockets_input_data[4] if len(sockets_input_data[4]) > 0 else [-180.0]
        v_2_angle_input: list = sockets_input_data[5] if len(sockets_input_data[5]) > 0 else [180.0]
        u_angle: list = sockets_input_data[6] if len(sockets_input_data[6]) > 0 else [270.0]

        #  Broadcast and calculate result
        data_tree: list = list(broadcast_data_tree(radius_1_input, radius_2_input, point_input, dir_input,
                                                   v_1_angle_input, v_2_angle_input, u_angle))
        torus: list = list(map_objects(data_tree, tuple, self.make_torus))

        return [torus]
