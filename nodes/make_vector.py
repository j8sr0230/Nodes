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
import awkward as ak

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon


@register_node
class MakeVector(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Make Vector"
    op_category = "Math"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(0, "X", 1, 1.0, True, ("int", "float")),
                                           (0, "Y", 1, 0.0, True, ("int", "float")),
                                           (0, "Z", 1, 0.0, True, ("int", "float"))],
                         outputs_init_list=[(1, "Vec", 0, 0, True, ("int", "float"))],
                         width=150)

    def eval_operation(self, sockets_input_data: list) -> list:
        # Inputs
        x_in = ak.Array(sockets_input_data[0])
        y_in = ak.Array(sockets_input_data[1])
        z_in = ak.Array(sockets_input_data[2])

        # Broadcast an zip to vector
        x_vector, y_vector, z_vector = ak.broadcast_arrays(x_in, y_in, z_in)
        res = ak.zip([x_vector, y_vector, z_vector])
        return [res.tolist()]
