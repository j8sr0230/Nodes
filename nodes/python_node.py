# -*- coding: utf-8 -*-
###################################################################################
#
#  python_node.py
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
from qtpy.QtWidgets import QSizePolicy, QTextEdit

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon


@register_node
class PythonNode(FCNNode):

    icon: str = icon("python_logo.png")
    op_title: str = "Python"
    op_category = "Experimental"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        width = 400
        super().__init__(scene=scene,
                         inputs_init_list=[(3, "Code", 4, "#enter python code\noutput_data=input_data",
                                            False, ("str", )),
                                           (0, "In", 0, "", True)],
                         outputs_init_list=[(0, "Out", 0, 0, True)],
                         width=width, auto_layout=False)

        # Manually set node and content size
        self.grNode.height = width
        self.grNode.default_height = width
        self.grNode.width = width
        self.content.setFixedHeight(self.grNode.height - self.grNode.title_vertical_padding -
                                    self.grNode.edge_padding - self.grNode.title_height)
        self.content.setFixedWidth(self.grNode.width - 2 * self.grNode.edge_padding)

        # Adjust content layout by expanding QTextEdit to maximum
        text_edit: QTextEdit = self.content.input_widgets[0]
        text_edit_policy: QSizePolicy = text_edit.sizePolicy()
        text_edit_policy.setVerticalStretch(QSizePolicy.Expanding)
        text_edit.setSizePolicy(text_edit_policy)

        text_edit.hide()  # Hack: Updates widget geometry to calculate the correct socket positions.
        text_edit.show()  # Hack: See above
        self.content.input_labels[0].setFixedHeight(text_edit.height())  # Levels heights of code label and widget

        # Update socket position
        self.place_sockets()

    def eval_operation(self, sockets_input_data: list) -> list:
        code: str = str(sockets_input_data[0][0])

        namespace = {'input_data': sockets_input_data[1], 'output_data': None}
        exec(code, namespace)
        return [namespace['output_data']]
