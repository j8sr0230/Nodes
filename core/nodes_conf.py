import importlib.util
import sys
import Exceptions as NodeException;
from os.path import dirname, basename, isfile, isdir, join
from glob import glob

import nodes_locator as locator

LISTBOX_MIMETYPE = "application/x-item"
DEBUG = False


class ConfException(Exception):
    pass


class InvalidNodeRegistration(ConfException):
    pass


class OpCodeNotRegistered(ConfException):
    pass


def register_node(class_reference):
    class_reference.op_code = str(class_reference)
    NodesStore.nodes[class_reference.op_code] = class_reference


class NodesStore:
    nodes = {}
    directories = [locator.NODES_PATH, ]

    def __new__(cls):
        return None

    @staticmethod
    def add_search_dir(path):
        if isdir(path) and path not in NodesStore.directories:
            NodesStore.directories.append(path)

    @staticmethod
    def get_class_from_opcode(op_code):
        if op_code not in NodesStore.nodes:
            raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
        return NodesStore.nodes[op_code]

    @staticmethod
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
            NodeException.nodesError("core","NodesStore","add_node_from_file",str(e));
            print(f'Unable to add node from "{nodes_file_path}": {e}')

    @staticmethod
    def refresh_nodes_list():
        NodesStore.nodes = {}
        for directory in NodesStore.directories:
            files = [f for f in glob(join(join(directory, "**"), "*.py"), recursive=True) if isfile(f)]
            for file_path in files:
                NodesStore.add_node_from_file(file_path)
