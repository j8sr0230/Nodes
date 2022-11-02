# -*- coding: utf-8 -*-
###################################################################################
#
#  alpha_test.py
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
from fcn_conf import register_node
from fcn_default_node import FCNNodeModel  # FCNNodeContentView
from fcn_locator import icon


@register_node
class Test(FCNNodeModel):

    icon: str = icon("fcn_default.png")
    op_title: str = "Test"
    op_category: str = "Alpha"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(6, "A", False), (6, "B", False)],
                         outputs_init_list=[(6, "Out", True)])

        self.grNode.resize(100, 80, 5)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def eval_operation(self, sockets_input_data: list) -> list:
        in_val: float = float(sockets_input_data[0][0])
        return [[in_val]]