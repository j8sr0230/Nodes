import os

from fcn_conf import register_node, OP_NODE_NUM_IN
from fcn_base_node import FCNNode


@register_node(OP_NODE_NUM_IN)
class NumberInput(FCNNode):
    """Number Input node.

    The Number Input node has an input field that can be used to enter any integer or fractional number. General
    instance independent data is stored in class variables. These are:
     - icon (str): Path to the node image, displayed in the node list box (QListWidget).
     - op_code (int): Unique index of the node, used to register the node in the app, referring to fcn_conf.py.
     - op_title (str): Title of the node, display in the node header.
    """

    icon: str = os.path.join(os.path.abspath(__file__), "..", "..", "icons", "fcn_default.png")
    op_code: int = OP_NODE_NUM_IN
    op_title: str = "Number Input"

    def __init__(self, scene):
        """Constructor of the NumberInput class.

        Calls the constructor of the parent class FCNNode.__init(scene, inputs_init_list, outputs_init_list, width,
        height). For more information see the FCNNode documentation in fcn_node_base.py.

        Note:
            Each init list has a set tuples as list items with the information for every socket. A single socket tuple
            has the signature
            (socket type (int),
             socket label (str),
             input widget type, referring to FCNGraphicsSocket.Socket_Input_Widget_Classes (int),
             default value (object),
             multi edge support (bool)).

        :param scene: Parent node of the socket.
        :type scene: Scene
        """

        super().__init__(scene=scene,
                         inputs_init_list=[(0, "In", 1, 0.0, False)], outputs_init_list=[(0, "Out", 0, 0.0, True)],
                         width=150, height=110)

    @staticmethod
    def eval_operation(sockets_input_data: list) -> list:
        """Returns the number from the input field or socket.

        Note:
            The general sockets_input_data list has the signature
            [[s0_e0, s0_e1, ..., s0_eN],
             [s1_e0, s1_e1, ..., s1_eN],
             ...,
             [sN_e0, sN_e1, ..., sN_eN]],
             where s stands for input socket and e for connected edge.

        :param sockets_input_data: Socket input data (signature see above).
        :type sockets_input_data: list
        :return: Calculated output data as list with one sublist per output socket, signature .
        :rtype: list
        """

        in_val: float = sockets_input_data[0][0]
        out_val: list = [in_val]
        result: list = [out_val]
        return result
