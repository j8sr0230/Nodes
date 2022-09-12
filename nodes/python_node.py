# -*- coding: utf-8 -*-
###################################################################################
#
#  text_input.py
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

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon

from nodeeditor.node_socket import LEFT_BOTTOM, RIGHT_BOTTOM, LEFT_CENTER, RIGHT_CENTER

@register_node
class PythonNode(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Python"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(3, "Code", 4, "#enter python code\noutput_data=input_data", False),
                                            (0, "In", 0, "", True)],
                         outputs_init_list=[(3, "Out", 0, 0, True)],
                         width=250)

    @staticmethod
    def eval_operation(sockets_input_data: list) -> list:
        code: str = str(sockets_input_data[0][0])

        namespace = {'input_data':sockets_input_data[1], 'output_data':None}
        try:
            exec(code, namespace)
            return [namespace['output_data']]
        except:
            return []
