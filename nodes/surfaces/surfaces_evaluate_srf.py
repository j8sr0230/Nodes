# -*- coding: utf-8 -*-
###################################################################################
#
#  surfaces_evaluate_srf.py
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
class EvaluateSurface(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Evaluate Srf"
    op_category: str = "Surfaces"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("U", True), ("V", True), ("Srf", True), ],
                         outputs_init_list=[("Point", True), ("Normal", True)])

        self.grNode.resize(120, 100)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

        self.flat_u_list: list = []
        self.flat_v_list: list = []
        self.flat_srf_list: list = []

    def evaluate_position(self, parameter_zip: tuple) -> list:
        surface: Part.Face = self.flat_srf_list[parameter_zip[0]]
        us: list = self.flat_u_list[parameter_zip[1]]
        vs: list = self.flat_v_list[parameter_zip[2]]

        us, vs = ak.broadcast_arrays(us, vs)
        res = []
        for i, u in enumerate(us):
            res.append(surface.valueAt(u, vs[i]))

        return res

    def evaluate_normal(self, parameter_zip: tuple) -> list:
        surface: Part.Face = self.flat_srf_list[parameter_zip[0]]
        us: list = self.flat_u_list[parameter_zip[1]]
        vs: list = self.flat_v_list[parameter_zip[2]]

        us, vs = ak.broadcast_arrays(us, vs)
        res = []
        for i, u in enumerate(us):
            res.append(surface.normalAt(u, vs[i]))

        return res

    def eval_operation(self, sockets_input_data: list) -> list:
        u_param: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [0]
        v_param: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [0]
        surfaces: list = sockets_input_data[2]

        # Array broadcast
        self.flat_srf_list: list = list(flatten(surfaces))
        srf_idx_list = map_objects(surfaces, Part.Face, lambda srf: self.flat_srf_list.index(srf))
        self.flat_u_list: list = list(simplify(u_param))
        u_idx_list: list = list(range(len(self.flat_u_list)))
        self.flat_v_list: list = list(simplify(v_param))
        v_idx_list: list = list(range(len(self.flat_v_list)))

        srf_idx_list, u_idx_list, v_idx_list = ak.broadcast_arrays(srf_idx_list, u_idx_list, v_idx_list)
        parameter_zip: list = ak.zip([srf_idx_list, u_idx_list, v_idx_list], depth_limit=None).tolist()

        pos_vectors: list = list(map_objects(parameter_zip, tuple, self.evaluate_position))
        normal_vectors: list = list(map_objects(parameter_zip, tuple, self.evaluate_normal))

        return [pos_vectors, normal_vectors]
