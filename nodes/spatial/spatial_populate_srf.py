# -*- coding: utf-8 -*-
###################################################################################
#
#  spatial_populate_srf.py
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
import random

import awkward as ak

from FreeCAD import Vector
import Part
import numpy as np

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import flatten, map_objects

from nodes_locator import icon


@register_node
class PopulateSrf(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Populate (Srf)"
    op_category: str = "Spatial"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Face", True), ("Count", False), ("Radius", False), ("Seed", False)],
                         outputs_init_list=[("Position", True)])  # , ("Normal", True)])

        self.seed: int = 0
        self.count: int = 10

        self.grNode.resize(130, 120)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def _check_min_radius(point, old_points, old_radiuses, min_r):
        if not old_points:
            return True
        old_points = np.array(old_points)
        old_radiuses = np.array(old_radiuses)
        point = np.array(point)
        distances = np.linalg.norm(old_points - point, axis=1)
        ok = (old_radiuses + min_r < distances).all()
        return ok

    def populate_positions(self, face: Part.Face) -> Part.Shape:
        # Get uv range of target face
        u_range: list = np.array(face.ParameterRange)[:2]
        v_range: list = np.array(face.ParameterRange)[2:]

        done = 0
        generated_verts = []
        generated_uv = []
        generated_radiuses = []

        while done < self.count:

            batch_us = []
            batch_vs = []
            left = self.count - done
            max_size = min(100, left)
            for i in range(max_size):
                u = random.uniform(u_range[0], u_range[1])
                v = random.uniform(v_range[0], v_range[1])
                batch_us.append(u)
                batch_vs.append(v)
            batch_us = np.array(batch_us)
            batch_vs = np.array(batch_vs)
            batch_ws = np.zeros_like(batch_us)
            batch_uvs = np.stack((batch_us, batch_vs, batch_ws)).T

            # surface.evaluate_array(batch_us, batch_vs)
            batch_verts = [face.valueAt(batch_us[i], batch_vs[i]) for i in range(max_size)]
            batch_verts = np.array([[v[0], v[1], v[2]] for v in batch_verts])
            batch_xs = batch_verts[:, 0]
            batch_ys = batch_verts[:, 1]
            batch_zs = batch_verts[:, 2]

            candidates = batch_verts
            candidate_uvs = batch_uvs


            print(candidates)
            done = done + 10


        # Generate random uv-points
        # u_list: list = list(np.random.uniform(low=u_range[0], high=u_range[1], size=self.count))
        # v_list: list = list(np.random.uniform(low=v_range[0], high=v_range[1], size=self.count))
        # uv_list = list(zip(u_list, v_list))
        #
        # return [face.valueAt(uv[0], uv[1]) for uv in uv_list if face.isInside(face.valueAt(uv[0], uv[1]), 0.1, True)]

    # def populate_normals(self, face: Part.Face) -> Part.Shape:
    #     # Get uv range of target face
    #     u_range: list = np.array(face.ParameterRange)[:2]
    #     v_range: list = np.array(face.ParameterRange)[2:]
    #
    #     # Generate random uv-points
    #     u_list: list = list(np.random.uniform(low=u_range[0], high=u_range[1], size=self.count))
    #     v_list: list = list(np.random.uniform(low=v_range[0], high=v_range[1], size=self.count))
    #     uv_list = list(zip(u_list, v_list))
    #
    #     return [face.normalAt(uv[0], uv[1]) for uv in uv_list if face.isInside(face.valueAt(uv[0], uv[1]), 0.1, True)]
        return [[0]]

    def eval_operation(self, sockets_input_data: list) -> list:
        face: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [None]
        self.count: int = int(sockets_input_data[1][0]) if len(sockets_input_data[1]) > 0 else 10
        self.seed: int = int(sockets_input_data[2][0]) if len(sockets_input_data[2]) > 0 else 0

        np.random.seed(self.seed)

        return [map_objects(face, Part.Face, self.populate_positions)]  # ,
                # map_objects(face, Part.Face, self.populate_normals)]
