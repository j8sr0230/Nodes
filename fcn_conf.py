import importlib.util
import sys
from os.path import dirname, basename, isfile, join
from glob import glob

import fcn_locator as locator

LISTBOX_MIMETYPE = "application/x-item"
FC_NODES = {
}
DEBUG = False
NODES_DIR = [locator.NODES_PATH, ]  # TODO: Add user's nodes directory from workbench pref


class ConfException(Exception):
    pass


class InvalidNodeRegistration(ConfException):
    pass


class OpCodeNotRegistered(ConfException):
    pass


def register_node(class_reference):
    class_reference.op_code = str(class_reference)
    FC_NODES[class_reference.op_code] = class_reference


def get_class_from_opcode(op_code):
    if op_code not in FC_NODES:
        raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return FC_NODES[op_code]


def add_node_from_file(nodes_file_path):
    module_name = basename(nodes_file_path)[:-3]
    spec = importlib.util.spec_from_file_location(module_name, nodes_file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
        if DEBUG:
            print(f'New node {module_name}')
    except Exception as e:
        print(f'Unable to add node from "{nodes_file_path}": {e}')


def refresh_nodes_list():
    global FC_NODES
    FC_NODES = {}
    for directory in NODES_DIR:
        files = [f for f in glob(join(directory, "*.py")) if isfile(f)]
        for file_path in files:
            add_node_from_file(file_path)


refresh_nodes_list()
