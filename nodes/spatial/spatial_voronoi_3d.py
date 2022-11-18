# -*- coding: utf-8 -*-
###################################################################################
#
#  spatial_voronoi_3d.py
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

from FreeCAD import Vector
import Part

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import map_last_level, map_objects, flatten, simplify

from nodes_locator import icon


@register_node
class Voronoi3D(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Voronoi (3D)"
    op_category: str = "Spatial"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Face", True), ("Point", True)],
                         outputs_init_list=[("Point", True)])

        self.face_list: list = []
        self.point_list: list = []

        self.grNode.resize(130, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def make_voronoi(object_zip: tuple) -> Part.Shape:
        face: Part.Face = object_zip[0]
        points: list = object_zip[1]

        base_pts = rand(20, 3) * 100
        vor = Voronoi(points=base_pts)
        #vor: Voronoi = Voronoi(np.array(points), qhull_options="QJ")
        print(vor.vertices)

        # Filter region for valid vectors
        # vor_points = vor.vertices
        # vor_regions = [vor_points[region].tolist() for region in vor.regions
        #                if all([-1 not in region]) and len(region) > 0]
        #
        # vector_vor_regions = map_last_level(vor_regions, float, lambda v: Vector(v[0], v[1], v[2]))
        #
        # valid_vector_regions: list = [[region] for region in vector_vor_regions
        #                               if all([face.isInside(vector, 1, True) for vector in region])]
        #
        # return valid_vector_regions

    def eval_operation(self, sockets_input_data: list) -> list:
        face: list = sockets_input_data[0]
        point: list = sockets_input_data[1]

        face_list: list = list(flatten(face))
        point_list: list = list(simplify(point))
        object_zip: list = list(zip(face_list, point_list))

        return [map_objects(object_zip, tuple, self.make_voronoi)]
