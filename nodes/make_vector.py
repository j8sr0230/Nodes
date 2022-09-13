# -*- coding: utf-8 -*-
###################################################################################
#
#  make_vector.py
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
import numpy as np
from FreeCAD import Vector

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon


@register_node
class MakeVector(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Make Vector"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(0, "X", 1, 1.0, True, ("int", "float")),
                                           (0, "Y", 1, 0.0, True, ("int", "float")),
                                           (0, "Z", 1, 0.0, True, ("int", "float"))],
                         outputs_init_list=[(1, "Vec", 0, 0, True, ("int", "float"))],
                         width=150)

    @staticmethod
    def eval_operation(sockets_input_data: list) -> list:
        # Inputs
        x_in = np.array(sockets_input_data[0], dtype=object)
        y_in = np.array(sockets_input_data[1], dtype=object)
        z_in = np.array(sockets_input_data[2], dtype=object)

        x_vector = x_in * np.array([1, 0, 0])
        y_vector = y_in * np.array([0, 1, 0])
        z_vector = z_in * np.array([0, 0, 1])

        res = x_vector + y_vector + z_vector
        return [[np.array(res).tolist()]]
