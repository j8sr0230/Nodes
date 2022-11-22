# -*- coding: utf-8 -*-
###################################################################################
#
#  spatial_voronoi_on_sld.py
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
import numpy as np
from scipy.spatial import Voronoi
from scipy import rand
from collections import defaultdict
import itertools


from FreeCAD import Vector
import Part

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import map_last_level, map_objects, flatten, simplify

from nodes_locator import icon


@register_node
class VoronoiOnSolid(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Voronoi on Sld"
    op_category: str = "Spatial"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Shape", True), ("Point", True), ("Inset", False)],
                         outputs_init_list=[("Point", True)])

        self.solid_list: list = []
        self.point_list: list = []
        self.inset: float = 0

        self.grNode.resize(130, 100)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def make_voronoi(object_zip: tuple) -> list:
        solid: Part.Solid = object_zip[0]
        points: list = object_zip[1]

        all_points: list = points
        box = solid.BoundBox

        x_min, x_max = box.XMin, box.XMax
        y_min, y_max = box.YMin, box.YMax
        z_min, z_max = box.ZMin, box.ZMax
        bounds = map_objects(list(itertools.product([x_min, x_max], [y_min, y_max], [z_min, z_max])), tuple,
                             lambda t: [t[0], t[1], t[2]])
        all_points.extend(bounds)

        vor = Voronoi(all_points)
        faces_per_solid = defaultdict(list)

        n_ridges = len(vor.ridge_points)
        for ridge_idx in range(n_ridges):
            site_idx_1, site_idx_2 = vor.ridge_points[ridge_idx]
            face = vor.ridge_vertices[ridge_idx]
            if -1 not in face:
                faces_per_solid[site_idx_1].append(face)
                faces_per_solid[site_idx_2].append(face)

        for solid_idx in sorted(faces_per_solid.keys()):
            for face in faces_per_solid[solid_idx]:
                print(solid_idx, face)

        return faces_per_solid

    def eval_operation(self, sockets_input_data: list) -> list:
        solid: list = sockets_input_data[0]
        point: list = sockets_input_data[1]
        self.inset: float = float(sockets_input_data[2][0]) if len(sockets_input_data[2]) > 0 else 0

        solid_list: list = list(flatten(solid))
        point_list: list = list(simplify(point))
        object_zip: list = list(zip(solid_list, point_list))

        return [map_objects(object_zip, tuple, self.make_voronoi)]
