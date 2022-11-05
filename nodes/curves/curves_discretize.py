# -*- coding: utf-8 -*-
###################################################################################
#
#  curves_discretize.py
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
import FreeCAD
import awkward as ak

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import flatten, map_objects

from nodes_locator import icon


@register_node
class DiscretizeCurve(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Discretize"
    op_category: str = "Curves"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Crv", True), ("Dist", True)],
                         outputs_init_list=[("Vec", True)])

        self.grNode.resize(100, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

        self.crv_list = []
        self.dist_list = []

    def discretize_curve(self, curve) -> list:
        vec_list = curve.discretize(self.dist_list.pop(0))
        return vec_list

    def eval_operation(self, sockets_input_data: list) -> list:
        curves: list = sockets_input_data[0]
        distances: list = sockets_input_data[1]

        # Force array broadcast
        self.crv_list: list = list(flatten(curves))
        crv_idx_list: list = list(range(len(self.crv_list)))
        crv_idx_list, distances = ak.broadcast_arrays(crv_idx_list, distances)
        self.dist_list = ak.flatten(distances, axis=None).tolist()

        vectors: list = [map_objects(curves, object, self.discretize_curve)]
        return [vectors]
