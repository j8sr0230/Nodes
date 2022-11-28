# -*- coding: utf-8 -*-
###################################################################################
#
#  curves_evaluate_crv.py
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
import Part
import awkward as ak

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import flatten, simplify, map_objects

from nodes_locator import icon


@register_node
class EvaluateCurve(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Evaluate Crv"
    op_category: str = "Curves"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Parameter", True), ("Curve", True), ],
                         outputs_init_list=[("Point", True), ("Tangent", True)])

        self.grNode.resize(120, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

        self.flat_crv_list: list = []
        self.flat_u_list: list = []

    def evaluate_position(self, parameter_zip: tuple) -> list:
        curve = self.flat_crv_list[parameter_zip[0]]
        us = self.flat_u_list[parameter_zip[1]]

        res = []
        if type(us) is list:
            for u in us:
                if isinstance(curve, Part.BSplineCurve) or isinstance(curve, Part.BezierCurve) \
                        or isinstance(curve, Part.Arc):
                    res.append(curve.value(u))
                else:
                    res.append(curve.valueAt(u))
        else:
            if isinstance(curve, Part.BSplineCurve) or isinstance(curve, Part.BezierCurve) \
                    or isinstance(curve, Part.Arc):
                res.append(curve.value(us))
            else:
                res.append(curve.valueAt(us))

        return res

    def evaluate_tangent(self, parameter_zip: tuple) -> list:
        curve = self.flat_crv_list[parameter_zip[0]]
        us = self.flat_u_list[parameter_zip[1]]

        res = []
        if type(us) is list:
            for u in us:
                if isinstance(curve, Part.BSplineCurve) or isinstance(curve, Part.BezierCurve) \
                        or isinstance(curve, Part.Arc):
                    res.append(curve.tangent(u))
                else:
                    res.append(curve.tangentAt(u))
        else:
            if isinstance(curve, Part.BSplineCurve) or isinstance(curve, Part.BezierCurve) \
                    or isinstance(curve, Part.Arc):
                res.append(curve.tangent(us))
            else:
                res.append(curve.tangentAt(us))

        return res

    def eval_operation(self, sockets_input_data: list) -> list:
        parameters: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [0]
        curves: list = sockets_input_data[1]

        # Array broadcasting
        self.flat_crv_list: list = list(flatten(curves))
        crv_idx_list = map_objects(curves, object, lambda crv: self.flat_crv_list.index(crv))
        self.flat_u_list: list = list(simplify(parameters))
        u_idx_list: list = list(range(len(self.flat_u_list)))

        crv_idx_list, u_idx_list = ak.broadcast_arrays(crv_idx_list, u_idx_list)
        parameter_zip: list = ak.zip([crv_idx_list, u_idx_list], depth_limit=None).tolist()

        pos_vectors: list = list(map_objects(parameter_zip, tuple, self.evaluate_position))
        tangent_vectors: list = list(map_objects(parameter_zip, tuple, self.evaluate_tangent))

        return [pos_vectors, tangent_vectors]
