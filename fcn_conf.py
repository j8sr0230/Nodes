LISTBOX_MIMETYPE = "application/x-item"

OP_NODE_FREE_ID = 1
FC_NODES = {
}


class ConfException(Exception):
    pass


class InvalidNodeRegistration(ConfException):
    pass


class OpCodeNotRegistered(ConfException):
    pass


def register_node(class_reference):
    global OP_NODE_FREE_ID
    class_reference.op_code = OP_NODE_FREE_ID
    FC_NODES[OP_NODE_FREE_ID] = class_reference
    OP_NODE_FREE_ID = max(OP_NODE_FREE_ID, op_code + 1)


def get_class_from_opcode(op_code):
    if op_code not in FC_NODES:
        raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return FC_NODES[op_code]


from nodes import *  # Import all nodes and register them
