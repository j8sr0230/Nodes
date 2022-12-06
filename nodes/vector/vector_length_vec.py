# -*- coding: utf-8 -*-
###################################################################################
#
#  vector_length_vec.py
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
from core.nodes_utils import map_objects
from core.nodes_default_node import FCNNodeModel

from nodes_locator import icon


@register_node
class VectorLength(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Length (Vec)"
    op_category: str = "Vector"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Vector", True)],
                         outputs_init_list=[("Length", True)])

        self.grNode.resize(130, 70)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def eval_operation(self, sockets_input_data: list) -> list:
        vector = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [Vector(1., 0., 0.)]

        return [map_objects(vector, Vector, lambda vec: vec.Length)]
