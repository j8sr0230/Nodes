# -*- coding: utf-8 -*-
###################################################################################
#
#  spatial_populate_2d.py
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
import numpy as np

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import flatten, map_objects

from nodes_locator import icon


@register_node
class Populate2D(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Populate (2D)"
    op_category: str = "Spatial"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Surface", True), ("Count", False), ("Seed", False)],
                         outputs_init_list=[("Points", True)])

        self.seed: int = 0
        self.count: int = 10

        self.grNode.resize(130, 100)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def populate_points(surface: Part.Face) -> Part.Shape:
        res = []

        # Get uv range of target face
        u_range = np.array(surface.ParameterRange)[:2]
        v_range = np.array(surface.ParameterRange)[2:]

        # Generate random uv-points
        u_list = np.interp(random_gen.beta(obj.UAlpha, obj.UBeta, number), [0, 1], uRange)
        v_list = np.interp(random_gen.beta(obj.VAlpha, obj.VBeta, number), [0, 1], vRange)
        print(u_range, v_range)

        return res

    def eval_operation(self, sockets_input_data: list) -> list:
        surface: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [None]
        self.count: int = int(sockets_input_data[1][0]) if len(sockets_input_data[1]) > 0 else 10
        self.seed: int = int(sockets_input_data[2][0]) if len(sockets_input_data[2]) > 0 else 0

        return [map_objects(surface, Part.Face, self.populate_points)]
