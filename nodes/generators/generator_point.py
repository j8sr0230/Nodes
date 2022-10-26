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

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon
from fcn_utils import map_objects


@register_node
class Point(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Point"
    op_category: str = "Generator"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(1, "Pos", 0, 0, True, ("vec", ))],
                         outputs_init_list=[(3, "Point", 0, 0, True, ("shape", ))],
                         width=150)

    @staticmethod
    def make_occ_point(position: tuple) -> Part.Shape:
        return Part.Point(App.Vector(position)).toShape()

    def eval_operation(self, sockets_input_data: list) -> list:
        pos: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [(0, 0, 0)]

        return [map_objects(pos, tuple, self.make_occ_point)]
