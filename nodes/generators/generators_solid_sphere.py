# -*- coding: utf-8 -*-
###################################################################################
#
#  generators_solid_sphere.py
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
import awkward as ak

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import flatten, map_objects

from nodes_locator import icon


@register_node
class Sphere(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Sphere"
    op_category: str = "Generators"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("R", True, ), ("Pos", True, )],
                         outputs_init_list=[("Sphere", True)])

        self.radius_list: list = []

        self.grNode.resize(120, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def make_occ_sphere(self, position: Vector) -> Part.Shape:
        return Part.makeSphere(self.radius_list.pop(0), position)

    def eval_operation(self, sockets_input_data: list) -> list:
        radius: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [10]
        pos: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [Vector(0, 0, 0)]

        # Force array broadcast
        pos_list: list = list(flatten(pos))
        pos_idx_list: list = list(range(len(pos_list)))
        radius, pos_idx_list = ak.broadcast_arrays(radius, pos_idx_list)

        self.radius_list = ak.flatten(radius, axis=None).tolist()

        return [map_objects(pos, Vector, self.make_occ_sphere)]
