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
from math import fabs

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

    icon: str = icon("nodes_voronoi3D.svg")
    op_title: str = "Voronoi on Sld"
    op_category: str = "Spatial"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Shape", True), ("Point", True), ("Mode", False), ("Scale", False)],
                         outputs_init_list=[("Shape", True)])

        self.solid_list: list = []
        self.point_list: list = []
        self.mode: int = 0
        self.scale: float = 0.9

        self.grNode.resize(130, 120)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def make_voronoi(self, object_zip: tuple) -> list:
        solid: Part.Solid = object_zip[0]
        points: list = object_zip[1]

        ###################################################################################
        # Based on https://github.com/nortikin/sverchok/blob/master/utils/voronoi3d.py
        box = solid.BoundBox
        x_min, x_max = box.XMin, box.XMax
        y_min, y_max = box.YMin, box.YMax
        z_min, z_max = box.ZMin, box.ZMax
        x_offset, y_offset, z_offset = fabs(x_max - x_min), fabs(y_max - y_min), fabs(z_max - z_min)
        bounds = list(itertools.product([x_min - x_offset, x_max + x_offset], [y_min - y_offset, y_max + y_offset],
                                        [z_min - z_offset, z_max + z_offset]))
        bounds = map_objects(bounds, tuple, lambda t: Vector(t[0], t[1], t[2]))
        all_points: np.ndarray = np.vstack((points, bounds))

        vor: Voronoi = Voronoi(all_points)

        # Generate voronoi solids from scipy.spatial.Voronoi data
        faces_per_solid = defaultdict(list)
        n_ridges = len(vor.ridge_points)

        for ridge_idx in range(n_ridges):
            site_idx_1, site_idx_2 = vor.ridge_points[ridge_idx]
            face = vor.ridge_vertices[ridge_idx]
            if -1 not in face:
                faces_per_solid[site_idx_1].append(face)
                faces_per_solid[site_idx_2].append(face)

        vor_solids: list = []
        for solid_idx in sorted(faces_per_solid.keys()):
            vor_faces: list = []
            for face in faces_per_solid[solid_idx]:
                face_vertices: list = vor.vertices[face].tolist()
                face_vectors = list(map_last_level(face_vertices, float, lambda v: Vector(v[0], v[1], v[2])))
        ###################################################################################

                segments = []
                for i in range(len(face_vectors)):
                    if i + 1 < len(face_vectors):
                        segments.append(Part.LineSegment(face_vectors[i], face_vectors[i + 1]))
                segments.append(Part.LineSegment(face_vectors[-1], face_vectors[0]))
                vor_faces.append(Part.Face(Part.Wire(Part.Shape(segments).Edges)))

            vor_solid: Part.Shape = Part.Solid(Part.Shell(vor_faces))
            if vor_solid.isValid():
                vor_solids.append(vor_solid)

        # Inner voronoi solids
        common: Part.Shape = solid.common(Part.makeCompound(vor_solids))
        difference: Part.Shape = solid.cut(common)
        inner_voronoi_solids: list = common.Solids + difference.Solids
        scaled_voronoi_solids: list = [solid.scale(self.scale, solid.CenterOfGravity) for solid in inner_voronoi_solids]

        if self.mode == 0:
            # Inner voronoi solids
            result: list = scaled_voronoi_solids
        elif self.mode == 1:
            # Inverse of inner voronoi solids
            base: Part.Shape = Part.Solid(solid)
            base.scale(self.scale, base.CenterOfGravity)
            cutter: Part.Shape = Part.makeCompound(scaled_voronoi_solids)
            result: list = base.cut(cutter).SubShapes
        elif self.mode == 2:
            # Inner voronoi faces
            base: Part.Shape = Part.Solid(solid).Shells[0]
            base.scale(self.scale, base.CenterOfGravity)
            cutter: Part.Shape = Part.makeCompound(scaled_voronoi_solids)
            result: list = base.common(cutter).SubShapes
        else:
            # Inverse of inner voronoi faces
            base: Part.Shape = Part.Solid(solid).Shells[0]
            base.scale(self.scale, base.CenterOfGravity)
            cutter: Part.Shape = Part.makeCompound(scaled_voronoi_solids)
            result: list = base.cut(cutter).SubShapes

        return result

    def eval_operation(self, sockets_input_data: list) -> list:
        solid: list = sockets_input_data[0]
        point: list = sockets_input_data[1]
        self.mode: int = int(sockets_input_data[2][0]) if len(sockets_input_data[2]) > 0 else 0
        self.scale: float = float(sockets_input_data[3][0]) if len(sockets_input_data[3]) > 0 else 0.9

        solid_list: list = list(flatten(solid))
        point_list: list = list(simplify(point))
        object_zip: list = list(zip(solid_list, point_list))

        return [map_objects(object_zip, tuple, self.make_voronoi)]
