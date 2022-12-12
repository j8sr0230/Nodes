# -*- coding: utf-8 -*-
###################################################################################
#
#  curves_helix.py
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
class Helix(FCNNodeModel):

    icon: str = icon("nodes_helix.svg")
    op_title: str = "Helix"
    op_category: str = "Curves"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Pitch", True), ("Height", True), ("Radius", True), ("Angle", True),
                                           ("Left", True)],
                         outputs_init_list=[("Shape", True)])

        self.grNode.resize(100, 140)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def make_helix(parameter_zip: tuple) -> Part.Shape:
        pitch_input: float = parameter_zip[0]
        height_input: float = parameter_zip[1]
        radius_input: float = parameter_zip[2]
        angle_input: float = parameter_zip[3]
        left_hand_input: bool = parameter_zip[4]

        return Part.makeHelix(pitch_input, height_input, radius_input, angle_input, left_hand_input)

    def eval_operation(self, sockets_input_data: list) -> list:
        # Get socket inputs
        pitch_input: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [10.0]
        height_input: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [100.0]
        radius_input: list = sockets_input_data[2] if len(sockets_input_data[2]) > 0 else [10.0]
        angle_input: list = sockets_input_data[3] if len(sockets_input_data[3]) > 0 else [10.0]
        left_hand_input: list = sockets_input_data[4] if len(sockets_input_data[4]) > 0 else [False]

        #  Broadcast and calculate result
        data_tree: list = list(broadcast_data_tree(pitch_input, height_input, radius_input, angle_input,
                                                   left_hand_input))
        cones: list = list(map_objects(data_tree, tuple, self.make_helix))

        return [cones]
