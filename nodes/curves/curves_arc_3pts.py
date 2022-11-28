# -*- coding: utf-8 -*-
###################################################################################
#
#  curves_arc_3pts.py
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
class Arc3Pts(FCNNodeModel):

    icon: str = icon("nodes_arc_3_pt.svg")
    op_title: str = "Arc (3 Pts)"
    op_category: str = "Curves"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Point 1", True), ("Point 2", True), ("Point 3", True)],
                         outputs_init_list=[("Shape", True)])

        self.point_1: list = []
        self.point_2: list = []
        self.point_3: list = []

        self.grNode.resize(120, 100)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def make_occ_arc(self, parameter_zip: tuple) -> Part.Shape:
        point_1 = self.point_1[parameter_zip[0]]
        point_2 = self.point_2[parameter_zip[1]]
        point_3 = self.point_3[parameter_zip[2]]

        return Part.Arc(point_1, point_2, point_3)

    def eval_operation(self, sockets_input_data: list) -> list:
        point_1: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [Vector(-5, 0, 0)]
        point_2: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [Vector(0, 5, 0)]
        point_3: list = sockets_input_data[2] if len(sockets_input_data[2]) > 0 else [Vector(5, 0, 0)]

        # Array broadcast
        self.point_1: list = list(flatten(point_1))
        p1_idx_list = map_objects(point_1, Vector, lambda vec: self.point_1.index(vec))
        self.point_2: list = list(flatten(point_2))
        p2_idx_list: list = list(range(len(self.point_2)))
        self.point_3: list = list(flatten(point_3))
        p3_idx_list: list = list(range(len(self.point_3)))

        p1_idx_list, p2_idx_list, p3_idx_list = ak.broadcast_arrays(p1_idx_list, p2_idx_list, p3_idx_list)
        parameter_zip: list = ak.zip([p1_idx_list, p2_idx_list, p3_idx_list], depth_limit=None).tolist()

        return [map_objects(parameter_zip, tuple, self.make_occ_arc)]
