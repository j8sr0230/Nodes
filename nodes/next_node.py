# -*- coding: utf-8 -*-
###################################################################################
#
#  next_node.py
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
from fcn_conf import register_node
from fcn_base_node import FCNNode

import fcn_locator as locator


@register_node
class NextNode(FCNNode):

    icon: str = locator.icon("fcn_default.png")
    op_title: str = "Next"
    op_category = "Animation"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene: 'Scene'):
        """Constructor of the SampleNode class.

        :param scene: Editor Scene in which the node is to be inserted.
        :type scene: Scene
        """

        inputs: list = [(6, "List", 1, 0, False), (0, "tick", 0, 0, True)]
        outputs: list = [(0, "Item", 0, 0, True)]
        width: int = 150
        self.index = 0

        super().__init__(scene=scene, inputs_init_list=inputs, outputs_init_list=outputs, width=width)

    def eval_operation(self, sockets_input_data: list) -> list:
        inputarray = sockets_input_data[0]
        if (not isinstance(inputarray, list)):
            return 0

        self.index +=1
        if self.index >= len(inputarray):
            self.index=0
        return [[inputarray[self.index]]]
