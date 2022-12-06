# -*- coding: utf-8 -*-
###################################################################################
#
#  modifiers_set_shape.py
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
import FreeCAD
import Part

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from nodes_locator import icon
from core.nodes_utils import flatten


@register_node
class SetShape(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Set Shape"
    op_category: str = "Modifiers"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Object", True), ("Shape", True)],
                         outputs_init_list=[("Object", True)])

        self.grNode.resize(120, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def eval_operation(self, sockets_input_data: list) -> list:
        object_input: list = sockets_input_data[0]
        shape_input: list = sockets_input_data[1]

        obj_list: list = list(flatten(object_input))
        shp_list: list = list(flatten(shape_input))

        if hasattr(FreeCAD, "ActiveDocument") and FreeCAD.ActiveDocument:
            for obj in obj_list:
                obj.Shape = shp_list.pop(0)

            FreeCAD.ActiveDocument.recompute()
        else:
            raise ValueError('No active document')

        return [object_input]
