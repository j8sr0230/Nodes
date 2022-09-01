import os
from math import floor

from qtpy.QtWidgets import QWidget, QLineEdit, QSlider
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget

from fcn_conf import register_node, OP_NODE_NUM_SLD
from fcn_base_node import FCNNode, FCNSocket, FCNNodeContentView


class NumberSliderContentView(FCNNodeContentView):
    def update_content_ui(self, sockets_input_data: list) -> None:
        slider_min: float = sockets_input_data[0][0]
        slider_max: float = sockets_input_data[1][0]
        slider_widget: QSlider = self.input_widgets[2]

        # Updates slider value according to the input values
        slider_widget.blockSignals(True)  # Prevents signal loop
        slider_widget.setRange(floor(slider_min), floor(slider_max))
        slider_widget.setValue(sockets_input_data[2][0])
        slider_widget.blockSignals(False)  # Reset signals


@register_node(OP_NODE_NUM_SLD)
class NumberSlider(FCNNode):

    icon: str = os.path.join(os.path.abspath(__file__), "..", "..", "icons", "fcn_default.png")
    op_code: int = OP_NODE_NUM_SLD
    op_title: str = "Number Slider"
    content_label_objname: str = "fcn_node_bg"

    NodeContent_class: QDMNodeContentWidget = NumberSliderContentView

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(0, "Min", 1, 0, False), (0, "Max", 1, 100, False),
                                           (0, "Val", 2, (0, 100, 50), False)],
                         outputs_init_list=[(0, "Out", 0, 0.0, True)],
                         width=250, height=160)

    @staticmethod
    def eval_operation(sockets_input_data: list) -> list:
        sld_val: float = sockets_input_data[2][0]
        out_val: list = [sld_val]
        result: list = [out_val]
        return result
