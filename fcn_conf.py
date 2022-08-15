LISTBOX_MIMETYPE = "application/x-item"

OP_NODE_INPUT = 1
OP_NODE_OUTPUT = 2
OP_NODE_ADD = 3
OP_NODE_SUB = 4
OP_NODE_MUL = 5
OP_NODE_DIV = 6

OP_NODE_TXT_IN = 7
OP_NODE_NUM_IN = 8
OP_NODE_NUM_SLID = 9
OP_NODE_NUMS_IN = 10
OP_NODE_OBJ_IN = 11
OP_NODE_VEC_XYZ = 12
OP_NODE_VEC_XYZ_IN = 13
OP_NODE_SET_SHP = 14
OP_NODE_BSPLINE_CRV = 15
OP_NODE_BASE = 16


FC_NODES = {
}


class ConfException(Exception):
    pass


class InvalidNodeRegistration(ConfException):
    pass


class OpCodeNotRegistered(ConfException):
    pass


def register_node_now(op_code, class_reference):
    if op_code in FC_NODES:
        raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s" % (
            op_code, FC_NODES[op_code]
        ))
    FC_NODES[op_code] = class_reference


def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class
    return decorator


def get_class_from_opcode(op_code):
    if op_code not in FC_NODES:
        raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return FC_NODES[op_code]


from nodes import *  # Import all nodes and register them
