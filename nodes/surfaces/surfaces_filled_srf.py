# -*- coding: utf-8 -*-
###################################################################################
#
#  surfaces_filled_surfaces.py
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
class FilledSurface(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Filled Srf"
    op_category: str = "Surfaces"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Bound", True), ("Support", True)],
                         outputs_init_list=[("Face", True)])

        self.grNode.resize(120, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def make_filled_face(parameter_zip: tuple) -> Part.Shape:
        bounds: list = parameter_zip[0].wrapped_data if hasattr(parameter_zip[0], 'wrapped_data') else None
        supports: list = parameter_zip[1].wrapped_data if hasattr(parameter_zip[1], 'wrapped_data') else None

        return Part.makeFilledFace(bounds + supports)

    def eval_operation(self, sockets_input_data: list) -> list:
        # Get socket inputs
        bound_input: list = [sockets_input_data[0]]
        support_input: list = [sockets_input_data[1]]

        # Needed, to treat list as atomic object during array broadcasting
        wrapped_bound_input: list = list(map_last_level(bound_input, Part.Shape | Part.BSplineCurve | Part.Arc,
                                                        ListWrapper))
        wrapped_support_input: list = list(map_last_level(support_input, Part.Shape | Part.BSplineCurve | Part.Arc,
                                                          ListWrapper))

        # Broadcast and calculate result
        data_tree: list = list(broadcast_data_tree(wrapped_bound_input, wrapped_support_input))
        filled_face: list = list(map_objects(data_tree, tuple, self.make_filled_face))

        return [filled_face]
