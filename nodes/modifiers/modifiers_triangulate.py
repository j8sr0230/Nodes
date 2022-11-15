# -*- coding: utf-8 -*-
###################################################################################
#
#  modifiers_triangulate.py
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

from FreeCAD import Vector
import Part
import Mesh
from MeshPart import meshFromShape

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import flatten, map_objects

from nodes_locator import icon


@register_node
class Triangulate(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Triangulate"
    op_category: str = "Modifiers"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Shape", True), ("Quality", False)],
                         outputs_init_list=[("Mesh", True)])

        self.quality: int = 0

        self.grNode.resize(110, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def make_mesh(self, shape: Part.Shape) -> Mesh.Mesh:
        return MeshPart.meshFromShape(Shape=shape, Fineness=self.quality, SecondOrder=0, Optimize=1, AllowQuad=0)

    def eval_operation(self, sockets_input_data: list) -> list:
        shape: list = sockets_input_data[0]
        self.quality: int = int(sockets_input_data[1][0]) if len(sockets_input_data[1]) > 0 else 0

        return [map_objects(shape, Part.Shape, self.make_mesh)]
