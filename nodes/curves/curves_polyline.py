# -*- coding: utf-8 -*-
###################################################################################
#
#  curves_polyline.py
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
from core.nodes_utils import flatten, map_last_level

from nodes_locator import icon


@register_node
class Polyline(FCNNodeModel):

    icon: str = icon("nodes_polyline.svg")
    op_title: str = "Polyline"
    op_category: str = "Curves"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Point", True), ("Closed", False)],
                         outputs_init_list=[("Shape", True)])

        self.grNode.resize(100, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

        self.is_closed = 0

    def make_occ_polyline(self, flat_points: list) -> Part.Shape:
        segments = []
        for i in range(len(flat_points)):
            if i + 1 < len(flat_points):
                segments.append(Part.LineSegment(flat_points[i], flat_points[i + 1]))

        if self.is_closed:
            segments.append(Part.LineSegment(flat_points[-1], flat_points[0]))

        return Part.Wire(Part.Shape(segments).Edges)

    def eval_operation(self, sockets_input_data: list) -> list:
        points: list = sockets_input_data[0] if len(list(flatten(sockets_input_data[0]))) > 1 else [Vector(0, 0, 0),
                                                                                                    Vector(10, 10, 0)]
        self.is_closed: bool = bool(sockets_input_data[1][0] if len(sockets_input_data[1]) > 0 else 0)

        return [[map_last_level(points, Vector, self.make_occ_polyline)]]
