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
class InletNode(FCNNode):

    icon: str = icon("arrow-right.png")
    op_title: str = "Inlet"
    op_category = "Utils"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        if hasattr(scene, 'inlets'):
            scene.inlets.append(self)
        else:
            scene.inlets = [self]

        self.data = []
        super().__init__(scene=scene,
                         inputs_init_list=[],
                         outputs_init_list=[(0, "Out", 0, 0, True)],
                         width=150)

        self.collapse_node(True)

    def setData(self, data):
        self.data = data

    def eval_operation(self, sockets_input_data: list) -> list:
        return [self.data]


@register_node
class OutletNode(FCNNode):

    icon: str = icon("arrow-right.png")
    op_title: str = "Outlet"
    op_category = "Utils"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):

        self.data = None
        if hasattr(scene, 'outlets'):
            scene.outlets.append(self)
        else:
            scene.outlets = [self]

        super().__init__(scene=scene,
                         inputs_init_list=[(0, "In", 0, 0, True)],
                         outputs_init_list=[],
                         width=150)

        self.collapse_node(True)


    def eval_operation(self, sockets_input_data: list) -> list:
        self.data = sockets_input_data[0]
        return None


@register_node
class SubPatchNode(FCNNode):

    icon: str = icon("fcn_wb_icon.svg")
    op_title: str = "SubPatch"
    op_category = "Utils"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        self.data = None
        self.sub_patch = None
        self.sub_window = None
        self.current_inputs = []
        self.current_outputs = []

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
            self.sub_patch._close_event_listeners = []
            self.sub_patch.add_close_event_listener(self.onClose)
        self.sub_window.show()

    def open(self):
        if self.sub_patch is None:
            # lazy import due to import loop if placed in header
            from fcn_sub_window import FCNSubWindow
            self.sub_patch = FCNSubWindow()
            self.sub_patch.fileNew()
            self.sub_patch.setWindowTitle("SubPatch")
            self.sub_patch.scene.addHasBeenModifiedListener(self.onChange)
            self.sub_patch.scene.addDropListener(self.onChange)

        if self.data is not None:
            self.sub_patch.scene.deserialize(self.data)

    def onChange(self, event=None):
        self.resetWidgets()
        self.sub_patch.setWindowTitle("SubPatch")

    def onClose(self, sub_window, event):
        self.data = self.sub_patch.scene.serialize()
        self.sub_window = None
        self.sub_patch = None

    def resetWidgets(self):
        sub_scene = self.sub_patch.scene
        inputs = []
        outputs = []
        if hasattr(sub_scene, 'inlets'):
            inputs = [(0, f"In {i}", 0, 0, True) for i, inlet in enumerate(sub_scene.inlets)]
        if hasattr(sub_scene, 'outlets'):
            outputs = [(0, f"Out {i}", 0, 0, True) for i, outlet in enumerate(sub_scene.outlets)]

        if self.current_inputs != inputs or self.current_outputs != outputs:
            # reinit
            self.initSockets(inputs, outputs)
            self.place_sockets()
            self.updateConnectedEdges()
            self.current_inputs = inputs
            self.current_outputs = outputs

    def eval_operation(self, sockets_input_data: list) -> list:
        self.open()

        sub_scene = self.sub_patch.scene
        if hasattr(sub_scene, 'inlets'):
            # sort sockets by vertical placement
            ordered_inlets = sorted(sub_scene.inlets, key=lambda inlet: inlet.pos.y())
            for i, input_data in enumerate(sockets_input_data):
                ordered_inlets[i].setData(input_data)
                ordered_inlets[i].markInvalid()
                ordered_inlets[i].eval()

        if hasattr(sub_scene, 'outlets'):
            ret = []
            for outlet in sorted(sub_scene.outlets, key=lambda outlet: outlet.pos.y()):
                outlet.markInvalid()
                outlet.eval()
                ret.append(outlet.data)
            return ret

        return None

    def serialize(self):
        res = super().serialize()
        res['data'] = self.data
        return res

    def deserialize(self, data: dict, hashmap=None, restore_id: bool = True, *args, **kwargs):
        if hashmap is None:
            hashmap = {}
        res = super().deserialize(data, hashmap, restore_id)
        try:
            self.data = data['data']
            self.open()
        except KeyError:
            self.data = None

        return res
