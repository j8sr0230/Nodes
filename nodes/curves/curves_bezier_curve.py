# -*- coding: utf-8 -*-
###################################################################################
#
#  curves_bezier_curve.py
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
from core.nodes_utils import flatten, map_last_level

from nodes_locator import icon


@register_node
class BezierCurve(FCNNodeModel):

    icon: str = icon("nodes_bezcurve.svg")
    op_title: str = "Bezier Crv"
    op_category: str = "Curves"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Point", True), ("Closed", False)],
                         outputs_init_list=[("Curve", True)])

        self.is_closed: bool = False

        self.grNode.resize(100, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def make_occ_bezier(self, flat_points: list) -> Part.Shape:
        if self.is_closed:
            flat_points.append(flat_points[0])

        curve = Part.BezierCurve()
        curve.setPoles(flat_points)
        return curve

    def eval_operation(self, sockets_input_data: list) -> list:
        points: list = sockets_input_data[0] if len(list(flatten(sockets_input_data[0]))) > 2 else [Vector(0, 0, 0),
                                                                                                    Vector(10, 0, 0),
                                                                                                    Vector(10, 10, 0)]
        self.is_closed: bool = bool(sockets_input_data[1][0] if len(sockets_input_data[1]) > 0 else 0)

        return [[map_last_level(points, Vector, self.make_occ_bezier)]]
