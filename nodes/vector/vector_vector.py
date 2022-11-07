# -*- coding: utf-8 -*-
###################################################################################
#
#  vector_vector.py
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
import awkward as ak

from core.nodes_default_node import FCNNodeModel
from core.nodes_conf import register_node
from core.nodes_utils import flatten, map_objects

from nodes_locator import icon


@register_node
class VectorIn(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Vector"
    op_category: str = "Vector"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("X", True), ("Y", True), ("Z", True)],
                         outputs_init_list=[("Vector", True)])

        self.grNode.resize(100, 100)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def eval_operation(self, sockets_input_data: list) -> list:
        # Inputs
        x_in = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [1]
        y_in = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [0]
        z_in = sockets_input_data[2] if len(sockets_input_data[2]) > 0 else [0]

        # Broadcast an zip to vector
        x_vector, y_vector, z_vector = ak.broadcast_arrays(x_in, y_in, z_in)

        res = ak.zip([x_vector, y_vector, z_vector]).tolist()
        return [map_objects(res, tuple, Vector)]
