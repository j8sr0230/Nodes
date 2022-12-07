# -*- coding: utf-8 -*-
###################################################################################
#
#  vector_scale_vec.py
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

from core.nodes_conf import register_node
from core.nodes_utils import map_objects, broadcast_data_tree
from core.nodes_default_node import FCNNodeModel

from nodes_locator import icon


@register_node
class ScaleVec(FCNNodeModel):

    icon: str = icon("nodes_vect_scale.svg")
    op_title: str = "Scale (Vec)"
    op_category: str = "Vector"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Vector", True), ("Factor", True)],
                         outputs_init_list=[("Out", True)])

        self.grNode.resize(120, 70)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def scale_vector(parameter_zip: tuple) -> Vector:
        vec: Vector = parameter_zip[0]
        scale: Vector = parameter_zip[1]

        return Vector(vec).scale(scale, scale, scale)

    def eval_operation(self, sockets_input_data: list) -> list:
        # Get socket inputs
        vector_input = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [Vector(1., 0., 0.)]
        scale_input = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [1]

        # Broadcast and calculate result
        data_tree: list = list(broadcast_data_tree(vector_input, scale_input))
        vectors: list = list(map_objects(data_tree, tuple, self.scale_vector))

        return [vectors]
