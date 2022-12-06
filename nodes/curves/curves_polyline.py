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
from FreeCAD import Vector
import Part

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import map_last_level, map_objects, broadcast_data_tree, ListWrapper

from nodes_locator import icon


@register_node
class Polyline(FCNNodeModel):

    icon: str = icon("nodes_polyline.svg")
    op_title: str = "Polyline"
    op_category: str = "Curves"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Point", True), ("Closed", True)],
                         outputs_init_list=[("Shape", True)])

        self.grNode.resize(100, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def make_polyline(parameter_zip: tuple) -> Part.Shape:
        points: list = parameter_zip[0].wrapped_data if hasattr(parameter_zip[0], 'wrapped_data') else None
        is_closed: bool = bool(parameter_zip[1])

        if points:
            segments = []
            for i in range(len(points)):
                if i + 1 < len(points):
                    segments.append(Part.LineSegment(points[i], points[i + 1]))
            if is_closed:
                segments.append(Part.LineSegment(points[-1], points[0]))

            return Part.Wire(Part.Shape(segments).Edges)

    def eval_operation(self, sockets_input_data: list) -> list:
        # Get socket inputs
        point_input: list = [sockets_input_data[0]] if len(sockets_input_data[0]) > 0 \
            else [[Vector(0, 0, 0), Vector(10, 10, 0)]]
        closed_input: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [False]

        # Needed, to treat list as atomic object during array broadcasting
        wrapped_point_input: list = list(map_last_level(point_input, Vector, ListWrapper))

        # Broadcast and calculate result
        data_tree: list = list(broadcast_data_tree(wrapped_point_input, closed_input))
        polylines: list = list(map_objects(data_tree, tuple, self.make_polyline))

        return [polylines]
