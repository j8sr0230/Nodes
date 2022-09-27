# -*- coding: utf-8 -*-
###################################################################################
#
#  object_input.py
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

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon


@register_node
class ObjectInput(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Object Input"
    op_category = "FreeCAD"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(3, "In", 1, "Object label", True, ("str", ))],
                         outputs_init_list=[(4, "Obj", 0, 0, True, ("fc_obj", ))],
                         width=150)

    def collapse_node(self, collapse: bool = False):
        super().collapse_node(collapse)

        if collapse is True:
            self.title = 'Obj: ' + self.content.input_widgets[0].text()
        else:
            self.title = self.default_title

    def eval_operation(self, sockets_input_data: list) -> list:
        label_list: list = sockets_input_data[0]
        obj_list: list = []

        if not (FreeCAD.ActiveDocument is None):
            for label in label_list:
                obj = FreeCAD.ActiveDocument.getObjectsByLabel(label)
                if len(obj) == 1:
                    obj_list.append(obj[0])
                else:
                    raise ValueError('Unknown object')
        else:
            raise Exception('No active document')

        return [obj_list]
