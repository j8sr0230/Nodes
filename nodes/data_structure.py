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
import numpy as np

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon
from fcn_utils import flatten_to_tuples


@register_node
class DataStructure(FCNNode):
    icon: str = icon("fcn_default.png")
    op_title: str = "Data Structure"
    op_category = "Lists"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(0, 'Op', 3, ['Graft', 'Flat', 'Flat Topo'], False, ('int', )),
                                           (6, 'In', 1, 0, True, ('*', ))],
                         outputs_init_list=[(6, 'Out', 0, 0, True, ('*', ))],
                         width=160)

    def collapse_node(self, collapse: bool = False):
        super().collapse_node(collapse)

        if collapse is True:
            self.title = self.content.input_widgets[0].itemText(self.sockets_input_data[0][0])
        else:
            self.title = self.default_title

    def eval_operation(self, sockets_input_data: list) -> list:
        self.collapse_node(self.content.isHidden())

        # Inputs
        op_code: int = sockets_input_data[0][0]
        in_array = sockets_input_data[1]

        # Outputs
        if op_code == 0:  # Graft
            res = [[val] for val in in_array]
        elif op_code == 1:  # Flat
            res = np.array(in_array).flatten().tolist()
        elif op_code == 2:  # Flat Topo
            res = flatten_to_tuples(in_array)
        else:
            raise ValueError("Unknown operation (Op)")
        return [res]
