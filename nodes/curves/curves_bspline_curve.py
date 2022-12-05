# -*- coding: utf-8 -*-
###################################################################################
#
#  curves_bspline_curve.py
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
from core.nodes_utils import map_objects, map_last_level, broadcast_data_tree, ListWrapper

from nodes_locator import icon


@register_node
class BSplineCurve(FCNNodeModel):

    icon: str = icon("nodes_bspline.svg")
    op_title: str = "BSpline Crv"
    op_category: str = "Curves"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Ctr Points", True), ("Closed", True)],
                         outputs_init_list=[("Curve", True)])

        self.grNode.resize(120, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def make_bspline(parameter_zip: tuple) -> Part.Shape:
        ctr_points: list = parameter_zip[0].wrapped_data if hasattr(parameter_zip[0], 'wrapped_data') else None
        is_closed: bool = bool(parameter_zip[1])

        if ctr_points:
            if is_closed:
                return Part.BSplineCurve(ctr_points, None, None, True, 3, None, False)
            else:
                return Part.BSplineCurve(ctr_points, None, None, False, 3, None, False)

    def eval_operation(self, sockets_input_data: list) -> list:
        point_input: list = [sockets_input_data[0]] if len(sockets_input_data[0]) > 0 \
            else [[Vector(0, 0, 0), Vector(10, 0, 0), Vector(10, 10, 0)]]
        closed_input: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [False]

        # Needed, to treat list as atomic object during array broadcasting
        wrapped_point_input: list = list(map_last_level(point_input, Vector, ListWrapper))

        # Broadcast and calculate result
        data_tree: list = list(broadcast_data_tree(wrapped_point_input, closed_input))
        bspline_curves: list = list(map_objects(data_tree, tuple, self.make_bspline))

        return [bspline_curves]
