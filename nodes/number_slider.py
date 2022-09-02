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
import os
from math import floor

from qtpy.QtWidgets import QWidget, QLineEdit, QSlider
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget

from fcn_conf import register_node, OP_NODE_FREE_ID
from fcn_base_node import FCNNode, FCNSocket, FCNNodeContentView


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


@register_node(OP_NODE_FREE_ID)
class NumberSlider(FCNNode):

    icon: str = os.path.join(os.path.abspath(__file__), "..", "..", "icons", "fcn_default.png")
    op_code: int = OP_NODE_FREE_ID
    op_title: str = "Number Slider"
    content_label_objname: str = "fcn_node_bg"

    NodeContent_class: QDMNodeContentWidget = NumberSliderContentView

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(0, "Min", 1, 0, False), (0, "Max", 1, 100, False),
                                           (0, "Val", 2, (0, 100, 50), False)],
                         outputs_init_list=[(0, "Out", 0, 0.0, True)],
                         width=250)

    @staticmethod
    def eval_operation(sockets_input_data: list) -> list:
        sld_val: float = sockets_input_data[2][0]
        out_val: list = [sld_val]
        result: list = [out_val]
        return result
