# -*- coding: utf-8 -*-
###################################################################################
#
#  number_input.py
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

from fcn_conf import register_node, OP_NODE_FREE_ID
from fcn_base_node import FCNNode


@register_node(OP_NODE_FREE_ID)
class NumberInput(FCNNode):

    icon: str = os.path.join(os.path.abspath(__file__), "..", "..", "icons", "fcn_default.png")
    op_code: int = OP_NODE_FREE_ID
    op_title: str = "Number Input"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(0, "In", 1, 0, False)], outputs_init_list=[(0, "Out", 0, 0, True)],
                         width=150, height=120)

    @staticmethod
    def eval_operation(sockets_input_data: list) -> list:
        in_val: float = sockets_input_data[0][0]
        out_val: list = [in_val]
        result: list = [out_val]
        return result
