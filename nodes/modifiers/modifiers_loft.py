# -*- coding: utf-8 -*-
###################################################################################
#
#  modifiers_loft.py
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
from FreeCAD import Vector
import Part

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import map_objects, map_last_level, broadcast_data_tree, ListWrapper

from nodes_locator import icon


@register_node
class Loft(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Loft"
    op_category: str = "Modifiers"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Shape", True), ("Solid", True), ("Ruled", True)],
                         outputs_init_list=[("Shape", True)])

        self.grNode.resize(100, 100)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def make_loft(parameter_zip: tuple) -> Part.Shape:
        sections: list = parameter_zip[0].wrapped_data if hasattr(parameter_zip[0], 'wrapped_data') else []
        solid: bool = parameter_zip[1]
        ruled: bool = parameter_zip[1]

        return Part.makeLoft(sections, solid, ruled)

    def eval_operation(self, sockets_input_data: list) -> list:
        # Get socket inputs
        shape_input: list = [sockets_input_data[0]]
        solid_input: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [True]
        ruled_input: list = sockets_input_data[2] if len(sockets_input_data[2]) > 0 else [False]

        # Needed, to treat list as atomic object during array broadcasting
        wrapped_shape_input: list = list(map_last_level(shape_input, Part.Shape | Part.BSplineCurve | Part.Arc,
                                                        ListWrapper))

        # Broadcast and calculate result
        data_tree: list = list(broadcast_data_tree(wrapped_shape_input, solid_input, ruled_input))
        lofts: list = list(map_objects(data_tree, tuple, self.make_loft))

        return [lofts]
