import os
from math import floor

from qtpy.QtWidgets import QWidget, QLineEdit, QSlider
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget

from fcn_conf import register_node, OP_NODE_NUM_SLD
from fcn_base_node import FCNNode, FCNSocket, FCNNodeContent


DEBUG = False


class NumberSliderContent(FCNNodeContent):
    def update_content_ui(self, sockets_input_data: list) -> None:
        slider_min: float = sockets_input_data[0][0]
        slider_max: float = sockets_input_data[1][0]

        slider_widget = self.input_widgets[2]

        slider_widget.blockSignals(True)  # Prevents signal loop
        slider_widget.setRange(floor(slider_min), floor(slider_max))
        slider_widget.setValue(sockets_input_data[2][0])
        slider_widget.blockSignals(False)  # Reset signals


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
    content_label_objname: str = "fcn_node_bg"

    NodeContent_class: QDMNodeContentWidget = NumberSliderContent

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
                         inputs_init_list=[(0, "Min", 1, 0, True), (0, "Max", 1, 10, True),
                                           (0, "Val", 2, (0, 10, 5), True)],
                         outputs_init_list=[(0, "Out", 0, 0.0, True)],
                         width=250, height=160)

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
