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
import os
from decimal import Decimal

import numpy as np
from FreeCAD import Vector
from Part import makeSphere

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon


@register_node
class ObjectInput(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Make Sphere"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(0, "R", 1, "10.0", False), (1, "Pos", 0, 0, True)],
                         outputs_init_list=[(5, "Shp", 0, 0, True)],
                         width=150)

    @staticmethod
    def eval_operation(sockets_input_data: list) -> list:
        sphere_radius: float = float(sockets_input_data[0][0])
        position_list: list = sockets_input_data[1]

        sphere_list = []
        for pos in position_list:
            sphere = makeSphere(sphere_radius, Vector(pos))
            sphere_list.append(sphere)

        return [sphere_list]
