import os

from fcn_conf import register_node, OP_NODE_FREE_ID
from fcn_base_node import FCNNode

import fcn_locator as locator


@register_node(OP_NODE_FREE_ID)
class A_Node(FCNNode):

    icon: str = locator.icon("fcn_default.png")
    op_code: int = OP_NODE_FREE_ID
    op_title: str = "A Node"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        # Definition of the input sockets
        #  socket_type (int) Only same type socket can connect
        #  socket_label (str)
        #  socket_widget_index (int) in 0 Empty, 1 QLineEdit, 2 QSlider, 3 QComboBox
        #  widget_default_value (obj) unused for Empty
        #                             string for QLineEdit
        #                             (min, max, step) for QLineEdit
        #                             list for QComboBox
        #  multi_edge (bool) True to allow multi wire from/to this socket
        inputs: list = [
                       (0, "First Input", 1, 0, False),
                       (0, "Second Input", 1, 0, True),
                       ]

        # Definition of the output sockets
        outputs: list = [
                        (0, "First Output", 0, 0, True),
                        (0, "Second Output", 0, 0, True),
                        ]

        width=150
        height=40*(len(inputs) + len(outputs) + 1)

        super().__init__(scene=scene,
                         inputs_init_list=inputs, outputs_init_list=outputs,
                         width=width, height=height)

    @staticmethod
    def eval_operation(sockets_input_data: list) -> list:
        # retrieve inputs datas
        first_in_val = sockets_input_data[0][0]

        # second index is the wire one in multi_edge case
        for value in sockets_input_data[1]:
            second_in_val += value  #add all values

        #compute output datas
        first_out_val: list = [first_in_val + second_in_val]
        second_out_val: list = [first_in_val - second_in_val]

        result: list = [first_out_val, second_out_val]
        return result
