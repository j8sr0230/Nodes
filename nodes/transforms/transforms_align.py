# -*- coding: utf-8 -*-
###################################################################################
#
#  transform_align.py
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
from math import degrees

import awkward as ak

from FreeCAD import Vector, Rotation
import Part

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import flatten, map_objects

from nodes_locator import icon


@register_node
class Align(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Align"
    op_category: str = "Transforms"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Shape", True), ("Shape Axis", True), ("Target Axis", True),
                                           ("Pivot", True)],
                         outputs_init_list=[("Shape", True)])

        self.grNode.resize(140, 120)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def make_alignment(parameter_zip: tuple) -> Part.Shape:
        shape: Part.Shape = parameter_zip[0]
        shp_axis: Vector = parameter_zip[1]
        target_axis: Vector = parameter_zip[2]
        pivot: Vector = parameter_zip[3]

        copy: Part.Shape = Part.Shape(shape)
        rot: Rotation = Rotation(shp_axis, target_axis)
        return copy.rotate(pivot, rot.Axis, degrees(rot.Angle))

    def eval_operation(self, sockets_input_data: list) -> list:
        # Get socket inputs
        shape_input: list = sockets_input_data[0]
        shape_axis_input: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [Vector(0, 0, 1)]
        target_axis_input: list = sockets_input_data[2] if len(sockets_input_data[2]) > 0 else [Vector(1, 0, 0)]
        pivot_input: list = sockets_input_data[3] if len(sockets_input_data[3]) > 0 else [Vector(0, 0, 0)]

        # Broadcast and calculate result
        data_tree: list = list(broadcast_data_tree(shape_input, shape_axis_input, target_axis_input, pivot_input))
        shapes: list = list(map_objects(data_tree, tuple, self.make_alignment))

        return [shapes]
