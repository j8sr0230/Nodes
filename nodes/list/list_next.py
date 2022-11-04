# -*- coding: utf-8 -*-
###################################################################################
#
#  list_next.py
#
#  Copyright (c) 2022 Florian Foinant-Willig <ffw@2f2v.fr>
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
from core.nodes_default_node import FCNNodeModel

import nodes_locator as locator


@register_node
class Next(FCNNodeModel):

    icon: str = locator.icon("nodes_default.png")
    op_title: str = "Next"
    op_category: str = "List"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        self.index: int = 0

        super().__init__(scene=scene, inputs_init_list=[("List", True), ("Tick", False)],
                         outputs_init_list=[("Item", True)])

        self.grNode.resize(100, 70)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def eval_operation(self, sockets_input_data: list) -> list:
        input_array = sockets_input_data[0] if len(sockets_input_data[0]) else [0]

        res = input_array[self.index]
        self.index += 1

        if self.index >= len(input_array):
            self.index = 0

        return [[res]]
