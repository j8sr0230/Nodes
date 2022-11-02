# -*- coding: utf-8 -*-
###################################################################################
#
#  number_scalar_math.py
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

from editor.nodes_conf import register_node
from editor.nodes_base_node import FCNNode
from nodes_locator import icon


@register_node
class ScalarMath(FCNNode):

    icon: str = icon("nodes_default.png")
    op_title: str = "Scalar Math"
    op_category: str = "Number"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(0, "Op", 3, ["a+b", "a-b", "a*b", "a/b", "a^b", ], False, ('int', )),
                                           (0, "a", 1, 1, True, ('float', 'int')),
                                           (0, "b", 1, 10, True, ('float', 'int'))],
                         outputs_init_list=[(0, "Res", 0, 11, True, ('float', 'int'))],
                         width=150)

    def collapse_node(self, collapse: bool = False):
        super().collapse_node(collapse)

        if collapse is True:
            self.title = "Math: " + self.content.input_widgets[0].currentText()
        else:
            self.title = self.default_title

    def eval_operation(self, sockets_input_data: list) -> list:
        # Inputs
        op_code: int = sockets_input_data[0][0]
        a_array = ak.Array(sockets_input_data[1])
        b_array = ak.Array(sockets_input_data[2])

        # Outputs
        if op_code == 0:  # Add
            res = a_array + b_array
        elif op_code == 1:  # Sub
            res = a_array - b_array
        elif op_code == 2:  # Mul
            res = a_array * b_array
        elif op_code == 3:  # Div
            res = a_array / b_array
        elif op_code == 4:  # Pow
            res = a_array ** b_array
        else:
            raise ValueError("Unknown operation (Op)")

        return [res.tolist()]
