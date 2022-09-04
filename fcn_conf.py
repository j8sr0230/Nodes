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


def register_node_now(op_code, class_reference):
    if op_code in FC_NODES:
        raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s" % (
            op_code, FC_NODES[op_code]
        ))
    FC_NODES[op_code] = class_reference
    global OP_NODE_FREE_ID
    OP_NODE_FREE_ID = max(OP_NODE_FREE_ID, op_code + 1)


def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class
    return decorator


def get_class_from_opcode(op_code):
    if op_code not in FC_NODES:
        raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return FC_NODES[op_code]

# Import nodes
import importlib.util
import sys
from os.path import dirname, basename, isfile, join
from glob import glob

import fcn_locator as locator

def add_node_from_file(file_path):
    module_name = basename(file_path)[:-3]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
        print(f'New node {module_name}')
    except Exception as e:
        print(f'Unable to add node from "{file_path}": {e}')

NODES_DIR = [locator.NODES_PATH,] #TODO add user's nodes directory from workbench pref

for directory in NODES_DIR:
    files = [f for f in glob(join(directory, "*.py")) if isfile(f)]
    for file_path in files:
        add_node_from_file(file_path)

# TODO allow to add node dynamicaly, needs GUI refresh
