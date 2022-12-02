# -*- coding: utf-8 -*-
###################################################################################
#
#  surfaces_uv_on_srf.py
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

import awkward as ak

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import flatten, map_objects

from nodes_locator import icon


@register_node
class UVOnSurface(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "UV on Srf"
    op_category: str = "Surfaces"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Surface", True), ("Point", True)],
                         outputs_init_list=[("U", True), ("V", True)])

        self.grNode.resize(100, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def evaluate_uv(parameter_zip: tuple) -> tuple:
        surface: Part.Face = parameter_zip[0]
        point: Vector = parameter_zip[1]

        uv: tuple = surface.Surface.parameter(point)
        return uv[0], uv[1]

    def eval_operation(self, sockets_input_data: list) -> list:
        surface_input: list = sockets_input_data[0]
        point_input: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [Vector(0, 0, 0)]

        # Array preprocessing
        surface_list: list = list(flatten(surface_input))
        point_list: list = list(flatten(point_input))
        surface_idx_tree: list = list(map_objects(surface_input, Part.Face, lambda srf: surface_list.index(srf)))
        point_idx_tree: list = list(map_objects(point_input, Vector, lambda vec: point_list.index(vec)))

        # Array broadcasting
        surface_idx_tree, point_idx_tree = ak.broadcast_arrays(surface_idx_tree, point_idx_tree)
        index_zip: list = ak.zip([surface_idx_tree, point_idx_tree], depth_limit=None).tolist()
        input_zip: list = list(map_objects(index_zip, tuple, lambda data: (surface_list[data[0]], point_list[data[1]])))

        # Calculate output and distribute result to sockets
        uvs: list = list(map_objects(input_zip, tuple, self.evaluate_uv))
        u_output: list = list(map_objects(uvs, tuple, lambda uv: uv[0]))
        v_output: list = list(map_objects(uvs, tuple, lambda uv: uv[1]))

        return [u_output, v_output]
