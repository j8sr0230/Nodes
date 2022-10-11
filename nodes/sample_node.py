# -*- coding: utf-8 -*-
###################################################################################
#
#  sample_node.py
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
from fcn_conf import register_node
from fcn_base_node import FCNNode

import fcn_locator as locator


@register_node
class DemoNode(FCNNode):

    icon: str = locator.icon("fcn_default.png")
    op_title: str = "Demo Node"
    op_category = "Demo Category"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene: 'Scene'):
        """Constructor of the DemoNode class.

        :param scene: Editor Scene in which the node is to be inserted.
        :type scene: Scene
        """

        # Definition of the input and output sockets with the signature
        # [(socket_type (int), socket_label (str), socket_widget_index (int), widget_default_value (obj),
        #   multi_edge (bool))].
        #
        # socket_type (int): Only same type socket can connect.
        # socket_label (str): Name of the socket.
        # socket_widget_index (int): 0 Empty, 1 QLineEdit, 2 QSlider, 3 QComboBox.
        # widget_default_value (obj): - Unused for Empty
        #                             - String for QLineEdit
        #                             - (Min, Max, Step) for QLineEdit
        #                             - List for QComboBox
        # multi_edge (bool): True, to allow multi edge connection from/to this socket.
        # socket_str_type(tuple): Allowed socket types as string (use "*" as wild card).
        inputs: list = [(0, "In 1", 1, 0, False, ("int", "float")), (0, "In 2", 1, 0, True, ("int",  "float"))]
        outputs: list = [(0, "Out 1", 0, 0, True, ("int", "float")), (0, "Out 2", 0, 0, True, ("int", "float"))]
        width: int = 150

        super().__init__(scene=scene, inputs_init_list=inputs, outputs_init_list=outputs, width=width)

    def eval_operation(self, sockets_input_data: list) -> list:
        """Calculation of the socket outputs.

        The eval_operation is responsible or the actual calculation of the socket outputs. It processes the input data
        structure passed in through the method parameter socket_input_data and returns the calculation result as a list,
        with one sublist per output socket.

        Note:
           The general sockets_input_data list has the signature
           [[s0_e0, s0_e1, ..., s0_eN],
            [s1_e0, s1_e1, ..., s1_eN],
            ...,
            [sN_e0, sN_e1, ..., sN_eN]],
            where s stands for input socket and e for connected edge.

        :param sockets_input_data: Socket input data.
        :type sockets_input_data: list
        :return: Calculated output data as a list with one sublist per output socket.
        :rtype: list
        """

        # Retrieve inputs data from the first connected edge of the first socket.
        first_in_val: float = float(sockets_input_data[0][0])

        # Retrieve inputs data from all connected edges of the second socket
        # (second index is the edge in multi_edge case).
        second_in_val: list = []
        for edge_value in sockets_input_data[1]:
            second_in_val.append(float(edge_value))  # Add all values

        # Compute output data
        first_out_val: list = [first_in_val + second_in_val[0]]
        second_out_val: list = [first_in_val - second_in_val[0]]

        # Return output data as a list with one sublist per output socket.
        return [first_out_val, second_out_val]
