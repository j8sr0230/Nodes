# -*- coding: utf-8 -*-
###################################################################################
#
#  number_slider.py
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
from math import floor
from decimal import Decimal

from qtpy.QtWidgets import QSlider
from nodeeditor.node_content_widget import QDMNodeContentWidget

from fcn_conf import register_node
from fcn_base_node import FCNNode, FCNNodeContentView
from fcn_locator import icon


class NumberSliderContentView(FCNNodeContentView):
    def update_content_ui(self, sockets_input_data: list) -> None:
        slider_min: float = sockets_input_data[0][0]
        slider_max: float = sockets_input_data[1][0]
        slider_widget: QSlider = self.input_widgets[2]

        # Updates slider value according to the input values
        slider_widget.blockSignals(True)  # Prevents signal loop
        slider_widget.setRange(floor(slider_min), floor(slider_max))
        slider_widget.setValue(sockets_input_data[2][0])
        slider_widget.blockSignals(False)  # Reset signals


@register_node
class NumberSlider(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Number Slider"
    op_category = "Inputs"
    content_label_objname: str = "fcn_node_bg"

    NodeContent_class: QDMNodeContentWidget = NumberSliderContentView

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(0, "Min", 1, 0, False, ("float", "int")),
                                           (0, "Max", 1, 100, False, ("float", "int")),
                                           (0, "Val", 2, (0, 100, 50), False, ("int", ))],
                         outputs_init_list=[(0, "Out", 0, 0.0, True, ("int", ))],
                         width=150)

    def collapse_node(self, collapse: bool = False) -> None:
        super().collapse_node(collapse)

        if collapse is True:
            self.title = 'In: %.2E' % Decimal(str(self.sockets_input_data[2][0]))
        else:
            self.title = self.default_title

    def eval_operation(self, sockets_input_data: list) -> list:
        self.collapse_node(self.content.isHidden())

        min_val: float = sockets_input_data[0][0]
        max_val: float = sockets_input_data[1][0]
        clamped_val: float = max(min(sockets_input_data[2][0], int(max_val)), int(min_val))

        return [[clamped_val]]
