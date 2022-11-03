# -*- coding: utf-8 -*-
###################################################################################
#
#  alpha_default_op.py
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
from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel  # FCNNodeContentView
from nodes_locator import icon


@register_node
class DefaultOp(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Op"
    op_category: str = "Alpha"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("A", False), ("B", False)],
                         outputs_init_list=[("Out", True)])

        # self.grNode.resize(100, 80)
        # for socket in self.inputs + self.outputs:
        # socket.setSocketPosition()

    def eval_operation(self, sockets_input_data: list) -> list:
        in_val: float = float(sockets_input_data[0][0])
        return [[in_val]]
