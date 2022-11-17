# -*- coding: utf-8 -*-
###################################################################################
#
#  spatial_voronoi_on_srf.py
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
import numpy as np
from scipy.spatial import Voronoi

from FreeCAD import Vector
import Part

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import map_last_level, map_objects, flatten, simplify

from nodes_locator import icon


@register_node
class VoronoiOnSrf(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Voronoi on Srf"
    op_category: str = "Spatial"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Face", True), ("Point", True), ("Scale", False)],
                         outputs_init_list=[("Wire", True)])

        self.scale: float = 1
        self.face_list: list = []
        self.point_list: list = []

        self.grNode.resize(130, 100)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def make_voronoi(self, parameter_zip: tuple) -> Part.Shape:
        face: Part.Face = self.face_list[parameter_zip[0]]
        points: list = self.point_list[parameter_zip[1]]

        point_array: np.array = np.array([[vector.x, vector.y] for vector in points])
        vor = Voronoi(point_array)
        return [Vector(v[0], v[1], 0) for v in vor.vertices]

    def eval_operation(self, sockets_input_data: list) -> list:
        face: list = sockets_input_data[0]
        point: list = sockets_input_data[1]
        self.scale: float = float(sockets_input_data[2][0]) if len(sockets_input_data[2]) > 0 else 1

        self.face_list: list = list(flatten(face))
        face_idx_list: list = list(map_objects(face, Part.Face, lambda f: self.face_list.index(f)))
        self.point_list: list = list(simplify(point))
        point_idx_list: list = list(range(len(self.point_list)))

        face_idx_list, point_idx_list = ak.broadcast_arrays(face_idx_list, point_idx_list)
        parameter_zip: list = ak.zip([face_idx_list, point_idx_list], depth_limit=None).tolist()

        return [map_objects(parameter_zip, tuple, self.make_voronoi)]
