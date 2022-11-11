# -*- coding: utf-8 -*-
###################################################################################
#
#  curves_evaluate.py
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
    op_title: str = "Evaluate"
    op_category: str = "Curves"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Parameter", True), ("Crv", True), ],
                         outputs_init_list=[("Pos", True), ("Tangent", True)])

        self.grNode.resize(120, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

        self.crv_list = []

    def evaluate_position(self, idx_param: tuple) -> list:
        curve = self.crv_list[idx_param[0]]
        param = idx_param[1]

        res = []
        if isinstance(curve, Part.BSplineCurve) or isinstance(curve, Part.Arc):
            res.append(curve.value(param))
        else:
            res.append(curve.valueAt(param))
        return res

    def evaluate_tangent(self, idx_param: tuple) -> list:
        curve = self.crv_list[idx_param[0]]
        param = idx_param[1]

        res = []
        if isinstance(curve, Part.BSplineCurve) or isinstance(curve, Part.Arc):
            res.append(curve.tangent(param))
        else:
            res.append(curve.tangentAt(param))
        return res

    def eval_operation(self, sockets_input_data: list) -> list:
        parameters: list = sockets_input_data[0]
        curves: list = sockets_input_data[1]

        # Array broadcasting
        self.crv_list: list = list(flatten(curves))
        crv_idx_list: list = list(range(len(self.crv_list)))
        crv_idx_list, parameters = ak.broadcast_arrays(crv_idx_list, parameters)
        idx_param_zip: list = ak.zip([crv_idx_list, parameters], depth_limit=None).tolist()

        pos_vector: list = list(map_objects(idx_param_zip, tuple, self.evaluate_position))
        tangent_vectors: list = list(map_objects(idx_param_zip, tuple, self.evaluate_tangent))

        return [pos_vector, tangent_vectors]
