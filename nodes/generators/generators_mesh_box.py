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

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import map_objects, broadcast_data_tree

from nodes_locator import icon


@register_node
class MeshBox(FCNNodeModel):

    icon: str = icon("nodes_mesh_cube.svg")
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

    @staticmethod
    def make_mesh_box(parameter_zip: tuple) -> Mesh.Mesh:
        width: Vector = parameter_zip[0]
        length: Vector = parameter_zip[1]
        height: Vector = parameter_zip[2]
        position: Vector = parameter_zip[3]

        box = Mesh.createBox(width, length, height)
        box.translate(position[0], position[1], position[2])
        return box

    def eval_operation(self, sockets_input_data: list) -> list:
        # Get socket inputs
        width_input: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [10]
        length_input: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [10]
        height_input: list = sockets_input_data[2] if len(sockets_input_data[2]) > 0 else [10]
        point_input: list = sockets_input_data[3] if len(sockets_input_data[3]) > 0 else [Vector(0, 0, 0)]

        #  Broadcast and calculate result
        data_tree: list = list(broadcast_data_tree(width_input, length_input, height_input, point_input))
        mesh_boxes: list = list(map_objects(data_tree, tuple, self.make_mesh_box))

        return [mesh_boxes]
