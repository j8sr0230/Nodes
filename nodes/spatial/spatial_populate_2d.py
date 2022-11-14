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
from typing import Optional

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
                         inputs_init_list=[("Face", True), ("Count", False), ("Seed", False)],
                         outputs_init_list=[("Positions", True), ("Normals", True)])

        self.seed: int = 0
        self.count: int = 10

        self.grNode.resize(130, 100)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def populate_positions(self, face: Part.Face) -> Part.Shape:
        # Get uv range of target face
        u_range: list = np.array(face.ParameterRange)[:2]
        v_range: list = np.array(face.ParameterRange)[2:]

        # Generate random uv-points
        u_list: list = list(np.random.uniform(low=u_range[0], high=u_range[1], size=self.count))
        v_list: list = list(np.random.uniform(low=v_range[0], high=v_range[1], size=self.count))
        uv_list = list(zip(u_list, v_list))

        return [face.valueAt(uv[0], uv[1]) for uv in uv_list if face.isInside(face.valueAt(uv[0], uv[1]), 0.1, True)]

    def populate_normals(self, face: Part.Face) -> Part.Shape:
        # Get uv range of target face
        u_range: list = np.array(face.ParameterRange)[:2]
        v_range: list = np.array(face.ParameterRange)[2:]

        # Generate random uv-points
        u_list: list = list(np.random.uniform(low=u_range[0], high=u_range[1], size=self.count))
        v_list: list = list(np.random.uniform(low=v_range[0], high=v_range[1], size=self.count))
        uv_list = list(zip(u_list, v_list))

        return [face.normalAt(uv[0], uv[1]) for uv in uv_list if face.isInside(face.valueAt(uv[0], uv[1]), 0.1, True)]

    def eval_operation(self, sockets_input_data: list) -> list:
        face: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [None]
        self.count: int = int(sockets_input_data[1][0]) if len(sockets_input_data[1]) > 0 else 10
        self.seed: int = int(sockets_input_data[2][0]) if len(sockets_input_data[2]) > 0 else 0

        np.random.seed(self.seed)

        return [map_objects(face, Part.Face, self.populate_positions),
                map_objects(face, Part.Face, self.populate_normals)]
