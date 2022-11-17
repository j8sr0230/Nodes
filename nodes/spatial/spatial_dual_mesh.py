# -*- coding: utf-8 -*-
###################################################################################
#
#  spatial_dual_mesh.py
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

from FreeCAD import Vector
import Part
import Mesh

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import map_objects

from nodes_locator import icon


@register_node
class DualMesh(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Dual Mesh"
    op_category: str = "Spatial"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Mesh", True), ("Scale", False)],
                         outputs_init_list=[("Wire", True)])

        self.scale: float = 1

        self.grNode.resize(110, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def make_dual_mesh(self, mesh: Mesh.Mesh) -> Part.Shape:
        # Generate list of all faces linked to the same mesh vertex
        linked_faces = []
        for point in mesh.Points:
            faces = [idx for idx, face in enumerate(mesh.Topology[1])
                     if (np.array(face) == point.Index).any()]
            linked_faces.append(faces)

        # Sort list linked_faces by neighbours
        for i in range(len(linked_faces)):
            faces = linked_faces[i]
            sorted_faces = [faces[0]]
            j = 1
            while j < len(faces):
                last_added = mesh.Facets[sorted_faces[-1]]
                for n in last_added.NeighbourIndices:
                    if n not in sorted_faces and n in faces:
                        sorted_faces.append(n)
                        break
                j = j + 1
            linked_faces[i] = sorted_faces

        shape_list = []
        for i, faces in enumerate(linked_faces):
            if len(faces) > 3:  # Al least three vectors

                # Faces are turned into vertices
                vectors = [mesh.Facets[tri].InCircle[0] for tri in faces]
                vectors.append(vectors[0])  # Close chain by first face for closed polygon

                # Generate wires
                wire = Part.makePolygon(vectors)
                scaled_wire = wire.scale(self.scale, wire.CenterOfMass)
                shape_list.append(scaled_wire)

                # face = Part.makeFilledFace(scaled_wire.Edges)
                # solid = face.extrude(obj.MeshLink[0].Mesh.Points[i].Normal * obj.Thickness)
                # solid.Tag = i  # Topological naming approach by realthunder
                # solid.Hasher = App.StringHasher()  # Topological naming approach by realthunder
                # solid.Hasher.Threshold = 10  # Topological naming approach by realthunder
                # shape_list.append(solid)

        return shape_list

    def eval_operation(self, sockets_input_data: list) -> list:
        mesh: list = sockets_input_data[0]
        self.scale: float = float(sockets_input_data[1][0]) if len(sockets_input_data[1]) > 0 else 1

        return [map_objects(mesh, Mesh.Mesh, self.make_dual_mesh)]
