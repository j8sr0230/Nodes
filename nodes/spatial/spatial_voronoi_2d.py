# -*- coding: utf-8 -*-
###################################################################################
#
#  spatial_voronoi_2d.py
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
class Voronoi2D(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Voronoi (2D)"
    op_category: str = "Spatial"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Points", True), ("Surface", True)],
                         outputs_init_list=[("Curve", True)])

        self.pos_list: list = []
        self.dir_list: list = []

        self.grNode.resize(120, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def make_occ_circle(self, r_pos_dir_zip: tuple) -> Part.Shape:
        radius = r_pos_dir_zip[0]
        position = self.pos_list[r_pos_dir_zip[1]]
        direction = self.dir_list[r_pos_dir_zip[2]]

        return Part.makeCircle(radius, position, direction)

    def eval_operation(self, sockets_input_data: list) -> list:
        radius: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [10]
        position: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [Vector(0, 0, 0)]
        direction: list = sockets_input_data[2] if len(sockets_input_data[2]) > 0 else [Vector(0, 0, 1)]

        # Array broadcast
        self.pos_list: list = list(flatten(position))
        pos_idx_list: list = list(range(len(self.pos_list)))
        self.dir_list: list = list(flatten(direction))
        dir_idx_list: list = list(range(len(self.dir_list)))

        radius, pos_idx_list, dir_idx_list = ak.broadcast_arrays(radius, pos_idx_list, dir_idx_list)
        parameter_zip: list = ak.zip([radius, pos_idx_list, dir_idx_list], depth_limit=None).tolist()

        return [map_objects(parameter_zip, tuple, self.make_occ_circle)]
