# -*- coding: utf-8 -*-
###################################################################################
#
#  script_python.py
#
#  Copyright (c) 2022 Florian Foinant-Willig <ffw@2f2v.fr>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
###################################################################################
from qtpy.QtWidgets import QSizePolicy, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from nodeeditor.node_content_widget import QTextEdit

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from nodes_locator import icon


class CodeEditorDialog(QDialog):
    layout: QVBoxLayout
    code_input_widget: QTextEdit
    ok_button: QPushButton
    cancel_button: QPushButton
    node: FCNNodeModel

    def __init__(self, node: FCNNodeModel = None, parent: QWidget = None):
        super().__init__(parent)
        self.init_ui()
        self.node = node

    def init_ui(self):
        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)

        # Code input widget
        self.code_input_widget: QTextEdit = QTextEdit("output_data = input_data\nprint(output_data)", self)
        self.layout.addWidget(self.code_input_widget)

        # Button row
        button_widget: QWidget = QWidget(self)
        button_widget_layout: QHBoxLayout = QHBoxLayout()
        button_widget_layout.setContentsMargins(0, 0, 0, 0)
        button_widget.setLayout(button_widget_layout)
        self.layout.addWidget(button_widget)

        self.ok_button: QPushButton = QPushButton("Ok")
        self.ok_button.clicked.connect(self.set_code)

        self.cancel_button: QPushButton = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.hide)

        button_widget_layout.addWidget(self.ok_button)
        button_widget_layout.addWidget(self.cancel_button)

    def set_code(self):
        self.node.code = self.code_input_widget.toPlainText()
        self.node.eval()
        self.hide()


@register_node
class PythonNode(FCNNodeModel):

    icon: str = icon("nodes_python_logo.png")
    op_title: str = "Python"
    op_category: str = "Script"
    content_label_objname: str = "fcn_node_bg"

    code_dialog: QDialog
    code: str

    def __init__(self, scene):
        self.code: srt = "output_data = input_data\nprint(output_data)"
        super().__init__(scene=scene, inputs_init_list=[("In", True)], outputs_init_list=[("Out", True)])

    def onDoubleClicked(self, event):
        self.code_dialog = CodeEditorDialog(node=self, parent=self.scene.getView())
        self.code_dialog.show()

    def eval_operation(self, sockets_input_data: list) -> list:
        namespace = {'input_data': sockets_input_data[0], 'output_data': None}
        exec(self.code, namespace)
        return [namespace['output_data']]
