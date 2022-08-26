LISTBOX_MIMETYPE = "application/x-item"

OP_NODE_NUM_IN = 1

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
