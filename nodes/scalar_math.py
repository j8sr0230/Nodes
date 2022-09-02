import os
from math import log

from fcn_conf import register_node, OP_NODE_FREE_ID
from fcn_base_node import FCNNode


@register_node(OP_NODE_FREE_ID)
class ScalarMath(FCNNode):

    icon: str = os.path.join(os.path.abspath(__file__), "..", "..", "icons", "fcn_default.png")
    op_code: int = OP_NODE_FREE_ID
    op_title: str = "Scalar Math"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(0, "Op", 3, ["Add", "Sub", "Mul", "Div", "Pow", "Log", ], False),
                                           (0, "a", 1, 1, False),
                                           (0, "b", 1, 10, False)],
                         outputs_init_list=[(0, "Res", 0, 11, True)],
                         width=150, height=180)

    @staticmethod
    def eval_operation(sockets_input_data: list) -> list:
        # Inputs
        op_code: int = sockets_input_data[0][0]
        a: float = sockets_input_data[1][0]
        b: float = sockets_input_data[2][0]

        # Outputs
        if op_code == 0:  # Add
            return [[a + b]]
        elif op_code == 1:  # Sub
            return [[a - b]]
        elif op_code == 2:  # Mul
            return [[a * b]]
        elif op_code == 3:  # Div
            return [[a / b]]
        elif op_code == 4:  # Pow
            return [[a ** b]]
        elif op_code == 5:  # Log
            return [[log(a, b)]]

        else:
            raise ValueError("Unknown operation (Op)")
