# -*- coding: utf-8 -*-
###################################################################################
#
#  data_structure.py
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

from fcn_conf import register_node
from fcn_base_node import FCNNode


@register_node
class DataStructure(FCNNode):
    icon: str = os.path.join(os.path.abspath(__file__), "..", "..", "icons", "fcn_default.png")
    op_title: str = "Data Structure"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(0, "Op", 3, ["Graft", "Flat", ], False), (0, "In", 1, 0, True)],
                         outputs_init_list=[(0, "Out", 0, 0, True)],
                         width=150)

    def collapse_node(self, collapse: bool = False):
        super().collapse_node(collapse)

        if collapse is True:
            self.title = self.content.input_widgets[0].currentText()
        else:
            self.title = self.default_title

    @staticmethod
    def eval_operation(sockets_input_data: list) -> list:
        # Inputs
        op_code: int = sockets_input_data[0][0]
        in_array = np.array(sockets_input_data[1])
        print(in_array)

        # Outputs
        if op_code == 0:  # Graft
            res = [[val] for val in in_array]
        elif op_code == 1:  # Flat
            res = [in_array.flatten()]
        else:
            raise ValueError("Unknown operation (Op)")
        return [res]
