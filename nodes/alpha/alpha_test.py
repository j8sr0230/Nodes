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
from decimal import Decimal

from qtpy.QtWidgets import QLineEdit
from nodeeditor.node_content_widget import QDMNodeContentWidget

from fcn_conf import register_node
from fcn_default_node import FCNNodeModel, FCNNodeContentView
from fcn_locator import icon


@register_node
class Test(FCNNodeModel):

    icon: str = icon("fcn_default.png")
    op_title: str = "Test"
    op_category: str = "Alpha"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(0, "In", 1, 0, False, ('int', 'float'))],
                         outputs_init_list=[(0, "Out", 0, 0, True, ('int', 'float'))],
                         width=150)

    def collapse_node(self, collapse: bool = False):
        super().collapse_node(collapse)

        if (collapse is True) and isinstance(self.sockets_input_data[0][0], (int, float)):
            self.title: str = 'In: %.2E' % Decimal(str(self.sockets_input_data[0][0]))
        else:
            self.title: str = self.default_title

    def eval_operation(self, sockets_input_data: list) -> list:
        self.collapse_node(self.content.isHidden())

        in_val: float = float(sockets_input_data[0][0])
        return [[in_val]]
