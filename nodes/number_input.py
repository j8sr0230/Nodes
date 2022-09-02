import os

from fcn_conf import register_node, OP_NODE_FREE_ID
from fcn_base_node import FCNNode


@register_node(OP_NODE_FREE_ID)
class NumberInput(FCNNode):

    icon: str = os.path.join(os.path.abspath(__file__), "..", "..", "icons", "fcn_default.png")
    op_code: int = OP_NODE_FREE_ID
    op_title: str = "Number Input"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(0, "In", 1, 0, False)], outputs_init_list=[(0, "Out", 0, 0, True)],
                         width=150, height=120)

    @staticmethod
    def eval_operation(sockets_input_data: list) -> list:
        in_val: float = sockets_input_data[0][0]
        out_val: list = [in_val]
        result: list = [out_val]
        return result
