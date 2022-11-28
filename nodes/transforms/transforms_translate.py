# -*- coding: utf-8 -*-
###################################################################################
#
#  transform_translate.py
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
import awkward as ak

from FreeCAD import Vector
import Part

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import flatten, map_objects

from nodes_locator import icon


@register_node
class Translate(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Translate"
    op_category: str = "Transforms"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Shape", True), ("Direction", True)],
                         outputs_init_list=[("Shape", True)])

        self.flat_shape_list: list = []
        self.flat_dir_list: list = []

        self.grNode.resize(120, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def make_occ_translation(self, parameter_zip: tuple) -> Part.Shape:
        shape: Part.Shape = self.flat_shape_list[parameter_zip[0]]
        direction: Vector = self.flat_dir_list[parameter_zip[1]]

        return shape.translate(direction)

    def eval_operation(self, sockets_input_data: list) -> list:
        shape: list = sockets_input_data[0]
        direction: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [Vector(0, 0, 1)]

        # Array broadcast
        self.flat_shape_list: list = list(flatten(shape))
        shape_idx_list = map_objects(shape, Part.Shape, lambda shp: self.flat_shape_list.index(shp))
        self.flat_dir_list: list = list(flatten(direction))
        dir_idx_list: list = list(range(len(self.flat_dir_list)))

        shape_idx_list, dir_idx_list = ak.broadcast_arrays(shape_idx_list, dir_idx_list)
        parameter_zip: list = ak.zip([shape_idx_list, dir_idx_list], depth_limit=None).tolist()

        return [map_objects(parameter_zip, tuple, self.make_occ_translation)]
