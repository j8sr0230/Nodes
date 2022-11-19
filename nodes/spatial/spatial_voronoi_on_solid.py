# -*- coding: utf-8 -*-
###################################################################################
#
#  spatial_voronoi_on_solid.py
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
                         inputs_init_list=[("Shape", True), ("Point", True)],
                         outputs_init_list=[("Point", True)])

        self.face_list: list = []
        self.point_list: list = []

        self.grNode.resize(130, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def voronoi3d_regions(points, closed_only=True, recalc_normals=True, do_clip=False, clipping=1.0):
        diagram = Voronoi(points)
        faces_per_point = defaultdict(list)
        nsites = len(diagram.point_region)
        nridges = len(diagram.ridge_points)
        open_sites = set()
        for ridge_idx in range(nridges):
            site_idx_1, site_idx_2 = diagram.ridge_points[ridge_idx]
            face = diagram.ridge_vertices[ridge_idx]
            if -1 in face:
                open_sites.add(site_idx_1)
                open_sites.add(site_idx_2)
                continue
            faces_per_point[site_idx_1].append(face)
            faces_per_point[site_idx_2].append(face)

        print(diagram.vertices)

        # new_verts = []
        # new_edges = []
        # new_faces = []
        #
        # for site_idx in sorted(faces_per_point.keys()):
        #     if closed_only and site_idx in open_sites:
        #         continue
        #     done_verts = dict()
        #     bm = bmesh.new()
        #     add_vert = bm.verts.new
        #     add_face = bm.faces.new
        #     for face in faces_per_point[site_idx]:
        #         face_bm_verts = []
        #         for vertex_idx in face:
        #             if vertex_idx not in done_verts:
        #                 bm_vert = add_vert(diagram.vertices[vertex_idx])
        #                 done_verts[vertex_idx] = bm_vert
        #             else:
        #                 bm_vert = done_verts[vertex_idx]
        #             face_bm_verts.append(bm_vert)
        #         add_face(face_bm_verts)
        #     bm.verts.index_update()
        #     bm.verts.ensure_lookup_table()
        #     bm.faces.index_update()
        #     bm.edges.index_update()
        #
        #     if closed_only and any(v.is_boundary for v in bm.verts):
        #         bm.free()
        #         continue
        #
        #     if recalc_normals:
        #         bm.normal_update()
        #         bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        #
        #     region_verts, region_edges, region_faces = pydata_from_bmesh(bm)
        #     bm.free()
        #     new_verts.append(region_verts)
        #     new_edges.append(region_edges)
        #     new_faces.append(region_faces)
        #
        # if do_clip:
        #     verts_n, edges_n, faces_n = [], [], []
        #     bounds = calc_bounds(points, clipping)
        #     for verts_i, edges_i, faces_i in zip(new_verts, new_edges, new_faces):
        #         bm = bmesh_from_pydata(verts_i, edges_i, faces_i)
        #         bmesh_clip(bm, bounds, fill=True)
        #         bm.normal_update()
        #         bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        #         verts_i, edges_i, faces_i = pydata_from_bmesh(bm)
        #         bm.free()
        #         verts_n.append(verts_i)
        #         edges_n.append(edges_i)
        #         faces_n.append(faces_i)
        #     new_verts, new_edges, new_faces = verts_n, edges_n, faces_n
        #
        # return new_verts, new_edges, new_faces

    def make_voronoi(self, object_zip: tuple) -> Part.Shape:
        face: Part.Face = object_zip[0]
        points: list = object_zip[1]

        self.voronoi3d_regions(np.array(points))

        # base_pts = rand(20, 3) * 100
        # vor = Voronoi(points=base_pts)
        # vor: Voronoi = Voronoi(np.array(points), qhull_options="QJ")
        # print(vor.vertices)

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
