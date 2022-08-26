import os

from fcn_conf import register_node, OP_NODE_NUM_IN
from nodes.fcn_base_node import FCNNode


@register_node(OP_NODE_NUM_IN)
class NumberInput(FCNNode):
    """Number input node.

    The Numbers node has an input field that can be used to enter any integer or fractional number. General instance
    independent data are stored in class variables. These are:
     - icon (str): Path to the node image, displayed in the node list box (QListWidget).
     - op_code (int): Unique index of the node, used to register the node in the app, referring to fcn_conf.py.
     - op_title (str): Title of the node, display in the node header.
    """

    icon: str = os.path.join(os.path.abspath(__file__), "..", "..", "icons", "fcn_default.png")
    op_code = OP_NODE_NUM_IN
    op_title = "Number"

    def __init__(self, scene):
        """Constructor of the FCNNode class.

        Calls the constructor of the parent class FCNNode.__init(scene, inputs_init_list, outputs_init_list, width,
        height). For more information see the FCNNode documentation in fcn_node_base.py.

        Note:
            Each socket list has a set tuples as list items with the information for every socket. A single socket tuple
            has the signature
            (socket type (int),
             socket label (str),
             input widget type (int),
             default value (object),
             multi edge support (bool)).

        :param scene: Parent node of the socket.
        :type scene: Scene
        """

        super().__init__(scene=scene,
                         inputs_init_list=[(0, "In", 1, 0.0, False)],
                         outputs_init_list=[(0, "Out", 0, 0.0, True)],
                         width=150, height=110)

    @staticmethod
    def eval_operation(sockets_input_data: list) -> list:
        """Returns the number from the input field or socket.

        Note:
            The general sockets_input_data list has the signature
            [[in_0_0, in_0_1, ..., in_0_N],
             [in_1_0, in_1_1, ..., in_1_N],
             ...,
             [in_N_0, in_N_1, ..., in_N_N]].

        :param sockets_input_data: Socket input data (signature see above).
        :type sockets_input_data: list
        :return: Calculated output data as list with one sublist per output socket, signature .
        :rtype: list
        """

        in1_val = sockets_input_data[0][0]
        out1_val = [in1_val]
        result = [out1_val]
        return result
