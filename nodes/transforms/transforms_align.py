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
                         inputs_init_list=[("Shape", True), ("Shape Axis", True), ("Target Axis", True)],
                         outputs_init_list=[("Shape", True)])

        self.flat_shape_list: list = []
        self.flat_shp_axis_list: list = []
        self.flat_target_axis_list: list = []

        self.grNode.resize(140, 100)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def make_alignment(self, parameter_zip: tuple) -> Part.Shape:
        shape: Part.Shape = self.flat_shape_list[parameter_zip[0]]
        shp_axis: Vector = self.flat_shp_axis_list[parameter_zip[1]]
        target_axis: Vector = self.flat_target_axis_list[parameter_zip[2]]

        copy: Part.Shape = Part.Shape(shape)
        rot: Rotation = Rotation(shp_axis, target_axis)
        return copy.rotate(shape.Placement.Base, rot.Axis, degrees(rot.Angle))

    def eval_operation(self, sockets_input_data: list) -> list:
        shape: list = sockets_input_data[0]
        shape_axis: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [Vector(0, 0, 1)]
        target_axis: list = sockets_input_data[2] if len(sockets_input_data[2]) > 0 else [Vector(1, 0, 0)]

        # Array broadcast
        self.flat_shape_list: list = list(flatten(shape))
        shape_idx_list = map_objects(shape, Part.Shape, lambda shp: self.flat_shape_list.index(shp))
        self.flat_shp_axis_list: list = list(flatten(shape_axis))
        shp_axis_idx_list: list = list(map_objects(shape_axis, Vector,
                                                   lambda vect: self.flat_shp_axis_list.index(vect)))
        self.flat_target_axis_list: list = list(flatten(target_axis))
        target_axis_idx_list: list = list(map_objects(target_axis, Vector,
                                                      lambda vect: self.flat_target_axis_list.index(vect)))

        shape_idx_list, shp_axis_idx_list, target_axis_idx_list = ak.broadcast_arrays(shape_idx_list, shp_axis_idx_list,
                                                                                      target_axis_idx_list)
        parameter_zip: list = ak.zip([shape_idx_list, shp_axis_idx_list, target_axis_idx_list],
                                     depth_limit=None).tolist()

        return [map_objects(parameter_zip, tuple, self.make_alignment)]
