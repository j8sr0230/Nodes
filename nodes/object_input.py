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
import os
from decimal import Decimal

import FreeCAD as App

from fcn_conf import register_node
from fcn_base_node import FCNNode


@register_node
class ObjectInput(FCNNode):

    icon: str = os.path.join(os.path.abspath(__file__), "..", "..", "icons", "fcn_default.png")
    op_title: str = "Object Input"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(3, "In", 1, "Object label", False)],
                         outputs_init_list=[(3, "Out", 0, 0, True)],
                         width=150)

    def collapse_node(self, collapse: bool = False):
        super().collapse_node(collapse)

        if collapse is True:
            self.title = 'Obj: ' + self.content.input_widgets[0].text()
        else:
            self.title = self.default_title

    @staticmethod
    def eval_operation(sockets_input_data: list) -> list:
        in_val: str = sockets_input_data[0][0]

        if not (App.ActiveDocument is None):
            obj_list = App.ActiveDocument.getObjectsByLabel(in_val)
            if len(obj_list) == 1:
                return [[obj_list[0]]]
            else:
                raise ValueError('Unknown object')
        else:
            raise Exception('No active document')
