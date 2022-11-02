# -*- coding: utf-8 -*-
###################################################################################
#
#  generator_solid_sphere.py
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
import FreeCAD as App
import Part
import awkward as ak

from editor.nodes_conf import register_node
from editor.nodes_base_node import FCNNode
from nodes_locator import icon
from editor.nodes_utils import simplify, map_objects


@register_node
class Sphere(FCNNode):

    icon: str = icon("nodes_default.png")
    op_title: str = "Solid Sphere"
    op_category: str = "Generator"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        self.radius_list: list = []

        super().__init__(scene=scene,
                         inputs_init_list=[(0, "R", 1, "10.0", True, ("int", "float")),
                                           (1, "Pos", 0, 0, True, ("vec", ))],
                         outputs_init_list=[(3, "Sphere", 0, 0, True, ("shape", ))],
                         width=150)

    def make_occ_sphere(self, position: tuple) -> Part.Shape:
        return Part.makeSphere(self.radius_list.pop(0), App.Vector(position))

    def eval_operation(self, sockets_input_data: list) -> list:
        radius: list = sockets_input_data[0]
        pos: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [(0, 0, 0)]

        # Force array broadcast
        pos_list: list = list(simplify(pos))
        pos_idx_list: list = list(range(len(pos_list)))
        radius, pos_idx_list = ak.broadcast_arrays(radius, pos_idx_list)

        self.radius_list = ak.flatten(radius, axis=None).tolist()

        return [map_objects(pos, tuple, self.make_occ_sphere)]
