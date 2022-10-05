# -*- coding: utf-8 -*-
###################################################################################
#
#  number_input.py
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
from fcn_base_node import FCNNode, FCNNodeContentView
from fcn_locator import icon


class NumberInputContentView(FCNNodeContentView):
    def update_content_ui(self, sockets_input_data: list) -> None:
        number_input: float = float(sockets_input_data[0][0])
        number_widget: QLineEdit = self.input_widgets[0]

        # Updates widget value according to the input values
        number_widget.blockSignals(True)  # Prevents signal loop
        number_widget.setText(str(number_input))
        number_widget.blockSignals(False)  # Reset signals


@register_node
class NumberInput(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Number Input"
    op_category = "Inputs"
    content_label_objname: str = "fcn_node_bg"

    NodeContent_class: QDMNodeContentWidget = NumberInputContentView

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(0, "In", 1, 0, False, ('int', 'float'))],
                         outputs_init_list=[(0, "Out", 0, 0, True, ('int', 'float'))],
                         width=150)

    def collapse_node(self, collapse: bool = False):
        super().collapse_node(collapse)

        if collapse is True:
            input_str = self.content.input_widgets[0].text()
            if input_str.isdigit():
                self.title = 'In: %.2E' % Decimal(self.content.input_widgets[0].text())
            else:
                self.title = 'In: ' + self.content.input_widgets[0].text()
        else:
            self.title = self.default_title

    def eval_operation(self, sockets_input_data: list) -> list:
        in_val: float = float(sockets_input_data[0][0])
        return [[in_val]]
