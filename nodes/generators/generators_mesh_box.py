# -*- coding: utf-8 -*-
###################################################################################
#
#  generators_mesh_box.py
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
import Mesh
import awkward as ak

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import flatten, map_objects

from nodes_locator import icon


@register_node
class MeshBox(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "MBox"
    op_category: str = "Generators"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Width", True,), ("Length", True), ("Height", True), ("Point", True)],
                         outputs_init_list=[("Mesh", True)])

        self.grNode.resize(100, 125)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

        self.width_list: list = []
        self.length_list: list = []
        self.height_list: list = []

    def make_mesh_box(self, position: Vector) -> Mesh.Mesh:
        box = Mesh.createBox(self.width_list.pop(0), self.length_list.pop(0), self.height_list.pop(0))
        box.translate(position[0], position[1], position[2])
        return box

    def eval_operation(self, sockets_input_data: list) -> list:
        width: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [10]
        length: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [10]
        height: list = sockets_input_data[2] if len(sockets_input_data[2]) > 0 else [10]
        pos: list = sockets_input_data[3] if len(sockets_input_data[3]) > 0 else [Vector(0, 0, 0)]

        # Force array broadcast
        pos_list: list = list(flatten(pos))
        pos_idx_list: list = list(range(len(pos_list)))
        width, length, height, pos_idx_list = ak.broadcast_arrays(width, length, height, pos_idx_list)

        self.width_list = ak.flatten(width, axis=None).tolist()
        self.length_list = ak.flatten(length, axis=None).tolist()
        self.height_list = ak.flatten(height, axis=None).tolist()

        return [map_objects(pos, Vector, self.make_mesh_box)]
