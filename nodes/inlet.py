# -*- coding: utf-8 -*-
###################################################################################
#
#  inlet.py
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
from fcn_locator import icon


@register_node
class InletNode(FCNNode):

    icon: str = icon("arrow-right.png")
    op_title: str = "Inlet"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        if hasattr(scene, 'inlets'):
            scene.inlets.append(self)
        else:
            scene.inlets = [self]

        self.data = []
        super().__init__(scene=scene,
                         inputs_init_list=[],
                         outputs_init_list=[(0, "Out", 0, 0, True)],
                         width=150)

        self.collapse_node(True)

    def setData(self, data):
        self.data = data

    def eval_operation(self, sockets_input_data: list) -> list:
        return [self.data]
