# -*- coding: utf-8 -*-
###################################################################################
#
#  scalar_math.py
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
from math import log

from fcn_conf import register_node
from fcn_base_node import FCNNode


@register_node
class ScalarMath(FCNNode):

    icon: str = os.path.join(os.path.abspath(__file__), "..", "..", "icons", "fcn_default.png")
    op_title: str = "Scalar Math"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(0, "Op", 3, ["Add", "Sub", "Mul", "Div", "Pow", "Log", ], False),
                                           (0, "a", 1, 1, False),
                                           (0, "b", 1, 10, False)],
                         outputs_init_list=[(0, "Res", 0, 11, True)],
                         width=150)

    @staticmethod
    def eval_operation(sockets_input_data: list) -> list:
        # Inputs
        op_code: int = sockets_input_data[0][0]
        a: float = sockets_input_data[1][0]
        b: float = sockets_input_data[2][0]

        # Outputs
        if op_code == 0:  # Add
            return [[a + b]]
        elif op_code == 1:  # Sub
            return [[a - b]]
        elif op_code == 2:  # Mul
            return [[a * b]]
        elif op_code == 3:  # Div
            return [[a / b]]
        elif op_code == 4:  # Pow
            return [[a ** b]]
        elif op_code == 5:  # Log
            return [[log(a, b)]]

        else:
            raise ValueError("Unknown operation (Op)")
