# -*- coding: utf-8 -*-
###################################################################################
#
#  sub_patch.py
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

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon, getFCNodesWorkbench


@register_node
class SubPatchNode(FCNNode):

    icon: str = icon("fcn_wb_icon.svg")
    op_title: str = "SubPatch"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        self.data = None
        self.sub_patch = None
        self.sub_window = None

        super().__init__(scene=scene,
                         inputs_init_list=[],
                         outputs_init_list=[],
                         width=150)

    def onDoubleClicked(self, event) -> None:
        self.open()
        self.show()

    def show(self):
        main_window = getFCNodesWorkbench().window
        if self.sub_window is not None:
            main_window.set_active_sub_window(self.sub_window)
        else:
            self.sub_window = main_window.create_mdi_child(self.sub_patch)
            self.sub_patch._close_event_listeners = [] # remove event_listener set by create_mdi_child
            self.sub_patch.add_close_event_listener(self.onClose)
        self.sub_window.show()

    def open(self):
        # lazy import due to import loop if placed in header
        from fcn_sub_window import FCNSubWindow
        self.sub_patch = FCNSubWindow()
        self.sub_patch.fileNew()
        self.sub_patch.setWindowTitle("SubPatch")
        self.sub_patch.scene.addHasBeenModifiedListener(self.onChange)

        if self.data is not None:
            self.sub_patch.scene.deserialize(self.data)
            self.resetWidgets()

    def onChange(self):
        self.resetWidgets()
        self.sub_patch.setWindowTitle("SubPatch")

    def onClose(self, sub_window, event):
        self.data = self.sub_patch.scene.serialize()
        self.sub_window = None

    def resetWidgets(self):
        sub_scene = self.sub_patch.scene
        inputs = []
        outputs = []
        if hasattr(sub_scene, 'inlets'):
            inputs = [(0, f"In {i}", 0, 0, True) for i, inlet in enumerate(sub_scene.inlets)]
        if hasattr(sub_scene, 'outlets'):
            outputs = [(0, f"Out {i}", 0, 0, True) for i, outlet in enumerate(sub_scene.outlets)]

        # reinit
        pos = self.grNode.pos
        self.remove()
        super().__init__(scene=self.scene,
                 inputs_init_list=inputs,
                 outputs_init_list=outputs,
                 width=150)
        self.grNode.pos = pos

    def eval_operation(self, sockets_input_data: list) -> list:
        if self.sub_patch is None:
            self.open()

        sub_scene = self.sub_patch.scene
        if hasattr(sub_scene, 'inlets'):
            for i, input_data in enumerate(sockets_input_data):
                sub_scene.inlets[i].setData(input_data[0])

        if hasattr(sub_scene, 'outlets'):
            ret = []
            for outlet in sub_scene.outlets:
                outlet.markInvalid()
                outlet.eval()
                ret.append(outlet.data)
            return ret

        return None
