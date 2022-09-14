# -*- coding: utf-8 -*-
###################################################################################
#
#  make_sphere.py
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
import Part

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon


@register_node
class MakePoint(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Make Point"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(1, "Pos", 0, 0, True, ("int", "float"))],
                         outputs_init_list=[(5, "Shp", 0, 0, True, ("Shape", ))],
                         width=150)

    def structure_to_vec(self, data_structure: list) -> list:
        if isinstance(data_structure, list) and len(data_structure) == 3 and \
                all(isinstance(i, float) for i in data_structure):
            # If data_structure is a vector
            yield Vector(data_structure)
        else:
            # If data is a sub list
            for sub_structure in data_structure:
                for elem in self.structure_to_vec(sub_structure):
                    yield elem

    def eval_operation(self, sockets_input_data: list) -> list:
        position_list: list = sockets_input_data[0]

        vertex_list = []
        vector_pos_lis = list(self.structure_to_vec(position_list))
        for vec in vector_pos_lis:
            vertex = Part.Point(vec).toShape()
            vertex_list.append(vertex)

        return [vertex_list]
