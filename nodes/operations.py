import os

from fcn_conf import register_node, OP_NODE_ADD, OP_NODE_SUB, OP_NODE_MUL, OP_NODE_DIV
from fcn_node_base import BaseNode


@register_node(OP_NODE_ADD)
class NumberAddNode(BaseNode):

    icon = os.path.join(os.path.abspath(__file__), "..", "..",  "icons", "fcn_default.png")
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = "+"
    content_label_objname = "calc_node_bg"

    def eval_operation(self, input1, input2):
        return input1 + input2


@register_node(OP_NODE_SUB)
class NumberSubNode(BaseNode):

    icon = os.path.join(os.path.abspath(__file__), "..", "..",  "icons", "fcn_default.png")
    op_code = OP_NODE_SUB
    op_title = "Subtract"
    content_label = "-"
    content_label_objname = "calc_node_bg"

    def eval_operation(self, input1, input2):
        return input1 - input2


@register_node(OP_NODE_MUL)
class NumberMulNode(BaseNode):

    icon = os.path.join(os.path.abspath(__file__), "..", "..",  "icons", "fcn_default.png")
    op_code = OP_NODE_MUL
    op_title = "Multiply"
    content_label = "*"
    content_label_objname = "calc_node_mul"

    def eval_operation(self, input1, input2):
        print('foo')
        return input1 * input2


@register_node(OP_NODE_DIV)
class NumberDivNode(BaseNode):

    icon = os.path.join(os.path.abspath(__file__), "..", "..",  "icons", "fcn_default.png")
    op_code = OP_NODE_DIV
    op_title = "Divide"
    content_label = "/"
    content_label_objname = "calc_node_div"

    def eval_operation(self, input1, input2):
        return input1 / input2
