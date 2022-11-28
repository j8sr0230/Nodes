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
from core.nodes_utils import flatten, simplify, map_objects

from nodes_locator import icon


@register_node
class UVOnSurface(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "UV on Srf"
    op_category: str = "Surfaces"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Srf", True), ("Point", True)],
                         outputs_init_list=[("U", True), ("V", True)])

        self.grNode.resize(100, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

        self.flat_srf_list: list = []
        self.flat_point_list: list = []

    def evaluate_u(self, parameter_zip: tuple) -> list:
        surface: Part.Face = self.flat_srf_list[parameter_zip[0]]
        points: list = self.flat_point_list[parameter_zip[1]]

        res: list = []
        if type(points) is list:
            for point in points:
                res.append(surface.Surface.parameter(point))
        else:
            res.append(surface.Surface.parameter(points)[0])

        return res

    def evaluate_v(self, parameter_zip: tuple) -> list:
        surface: Part.Face = self.flat_srf_list[parameter_zip[0]]
        points: list = self.flat_point_list[parameter_zip[1]]

        res: list = []
        if type(points) is list:
            for point in points:
                res.append(surface.Surface.parameter(point))
        else:
            res.append(surface.Surface.parameter(points)[1])

        return res

    def eval_operation(self, sockets_input_data: list) -> list:
        surfaces: list = sockets_input_data[0]
        point: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [Vector(0, 0, 0)]

        # Array broadcast
        self.flat_srf_list: list = list(flatten(surfaces))
        srf_idx_list = map_objects(surfaces, Part.Face, lambda srf: self.flat_srf_list.index(srf))
        self.flat_point_list: list = list(flatten(point))
        point_idx_list = map_objects(point, Vector, lambda vec: self.flat_point_list.index(vec))

        srf_idx_list, point_idx_list = ak.broadcast_arrays(srf_idx_list, point_idx_list)
        parameter_zip: list = ak.zip([srf_idx_list, point_idx_list], depth_limit=None).tolist()

        us: list = list(map_objects(parameter_zip, tuple, self.evaluate_u))
        vs: list = list(map_objects(parameter_zip, tuple, self.evaluate_v))

        return [us, vs]
