import os
from math import floor

from qtpy.QtWidgets import QWidget, QLineEdit, QSlider
from nodeeditor.node_node import Node

from fcn_conf import register_node, OP_NODE_NUM_SLD
from nodes.fcn_base_node import FCNNode, FCNSocket


DEBUG = False


@register_node(OP_NODE_NUM_SLD)
class NumberSlider(FCNNode):
    """Number Slider node.

    The Number Slider node has two input fields and the actual slider. The input fields Min and Max can be used, to set
    the slider range. The precision o the slider value is driven by the value of the lower slider range (Min). General
    instance independent data is stored in class variables.
    These are:
     - icon (str): Path to the node image, displayed in the node list box (QListWidget).
     - op_code (int): Unique index of the node, used to register the node in the app, referring to fcn_conf.py.
     - op_title (str): Title of the node, display in the node header.
    """

    icon: str = os.path.join(os.path.abspath(__file__), "..", "..", "icons", "fcn_default.png")
    op_code: int = OP_NODE_NUM_SLD
    op_title: str = "Number Slider"

    def __init__(self, scene):
        """Constructor of the NumberSlider class.

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
                         inputs_init_list=[(0, "Min", 1, 0, False), (0, "Max", 1, 10, False), (0, "Val", 2, 5, False)],
                         outputs_init_list=[(0, "Out", 0, 0.0, True)],
                         width=250, height=160)

    def eval_preparation(self) -> list:
        """Prepares the evaluation of the output socket values.

        This method prepares the actual calculation of the socket output data. Input values are collected from connected
        nodes or socket input widgets, stored in a list data structure and passed to the eval_operation method. After
        successful calculation, this method sends the result back to the top level eval method.

        Note:
            All output sockets are evaluated. The resulting data structure is returned and passed to the data class
            attribute.

        :return: Calculated output data structure with all socket outputs.
        :rtype: list
        """

        # TODO: Eval just once by saving results in socket and pulling them into eval method (i. e. update_sockets())
        self.update_content_status()  # Update node content widgets

        # Build input data structure
        has_slider = False
        sockets_input_data: list = []  # Container for input data
        for socket in self.inputs:
            socket_input_data: list = []

            if isinstance(socket.grSocket.input_widget, QSlider):
                has_slider = True

            if socket.hasAnyEdge():
                # From connected nodes
                for edge in socket.edges:
                    other_socket: FCNSocket = edge.getOtherSocket(socket)
                    other_socket_node: Node = other_socket.node
                    other_socket_index: int = other_socket.index
                    other_socket_value_list: list = other_socket_node.eval(other_socket_index)
                    for other_socket_value in other_socket_value_list:
                        socket_input_data.append(other_socket_value)
            else:
                # From input data widgets
                socket_input_widget: QWidget = socket.grSocket.input_widget
                if socket_input_widget is not None:
                    if isinstance(socket_input_widget, QLineEdit):
                        input_value: float = float(socket_input_widget.text())
                        socket_input_data.append(input_value)

                    elif isinstance(socket_input_widget, QSlider):
                        input_value = socket_input_widget.value()
                        socket_input_data.append(input_value)

            sockets_input_data.append(socket_input_data)

        if has_slider is True:
            # Widget property update during runtime, which is not covered by update_content_status,
            # i.e. inputs from other sockets.
            slider_min: float = sockets_input_data[0][0]
            slider_max: float = sockets_input_data[1][0]

            slider_widget = self.content.input_widgets[2]

            slider_widget.blockSignals(True)  # Prevents signal loop
            slider_widget.setRange(floor(slider_min), floor(slider_max))
            slider_widget.setValue(sockets_input_data[2][0])
            slider_widget.blockSignals(False)  # Reset signals

        sockets_output_data: list = self.eval_operation(sockets_input_data)  # Calculate socket output
        self.data: list = sockets_output_data
        self.markDirty(False)
        self.markInvalid(False)
        self.grNode.setToolTip(str(self.data))
        self.markDescendantsDirty()
        self.evalChildren()
        if DEBUG:
            print("%s::__eval()" % self.__class__.__name__, "self.data = ", self.data)
        return sockets_output_data

    @staticmethod
    def eval_operation(sockets_input_data: list) -> list:
        """Returns the number from slider widget or socket.

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

        sld_val: float = sockets_input_data[2][0]

        out_val: list = [sld_val]
        result: list = [out_val]
        return result
