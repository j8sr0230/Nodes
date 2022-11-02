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

from nodeeditor.node_edge import Edge, EDGE_TYPE_BEZIER

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
        self.scene = scene
        self.data = []

        if hasattr(scene, 'inlets'):
            scene.inlets.append(self)
        else:
            scene.inlets = [self]

        super().__init__(scene=scene,
                         inputs_init_list=[],
                         outputs_init_list=[(0, "Out", 0, 0, True)],
                         width=150)

        self.collapse_node(True)

    def remove(self):
        self.scene.inlets.remove(self)
        self.scene.container.resetWidgets()
        super().remove()

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
        self.scene = scene
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

    def remove(self):
        self.scene.outlets.remove(self)
        self.scene.container.resetWidgets()
        super().remove()

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
        self.sub_window = None
        self.sub_editor = None
        self.sub_scene_data = None

        super().__init__(scene=scene,
                         inputs_init_list=[],
                         outputs_init_list=[],
                         width=150)

    def get_sub_editor(self):
        if self.sub_editor is None:
            # lazy import due to import loop if placed in header
            from fcn_sub_window import FCNSubWindow

            self.sub_editor = FCNSubWindow()
            self.sub_editor.fileNew()
            self.sub_editor.setWindowTitle("SubPatch")

            sub_scene = self.sub_editor.scene
            sub_scene.deserialize(self.sub_scene_data)
            sub_scene.addHasBeenModifiedListener(self.onChange)
            sub_scene.addDropListener(self.onChange)
            sub_scene.container = self
        return self.sub_editor

    def get_sub_scene(self):
        return self.get_sub_editor().scene

    def onDoubleClicked(self, event) -> None:
        main_window = getFCNodesWorkbench().window
        if self.sub_window is not None:
            main_window.set_active_sub_window(self.sub_window)
        else:
            sub_editor = self.get_sub_editor()
            self.sub_window = main_window.create_mdi_child(sub_editor)
            sub_editor._close_event_listeners = []
            sub_editor.add_close_event_listener(self.onClose)
        self.sub_window.show()

    def onChange(self, event=None):
        self.resetWidgets()
        self.sub_scene_data = self.get_sub_scene().serialize()
        self.get_sub_editor().setWindowTitle("SubPatch")

    def onClose(self, sub_window, event):
        self.sub_window = None
        self.sub_editor = None

    def resetWidgets(self):
        self.markInvalid()

        # save and delete edges
        starts = []
        for i in self.inputs:
            edges_start = []
            for edge in i.edges:
                edges_start.append(edge.start_socket)
                edge.remove()
            starts.append(edges_start)
        ends = []
        for o in self.outputs:
            edges_end = []
            for edge in o.edges:
                edges_end.append(edge.end_socket)
                edge.remove()
            ends.append(edges_end)

        # reinit
        inputs = []
        outputs = []
        sub_scene = self.get_sub_scene()
        if hasattr(sub_scene, 'inlets'):
            inputs = [(0, f"In {i}", 0, 0, True) for i, inlet in enumerate(sub_scene.inlets)]
        if hasattr(sub_scene, 'outlets'):
            outputs = [(0, f"Out {i}", 0, 0, True) for i, outlet in enumerate(sub_scene.outlets)]
        self.initSettings()
        self.initSockets(inputs, outputs)
        self.place_sockets()

        # restore edges
        for i, end in enumerate(self.inputs):
            try:
                for start in starts[i]:
                    Edge(self.scene, start, end, EDGE_TYPE_BEZIER)
            except IndexError:
                break
        for i, start in enumerate(self.outputs):
            try:
                for end in ends[i]:
                    Edge(self.scene, start, end, EDGE_TYPE_BEZIER)
            except IndexError:
                break

        self.updateConnectedEdges()
        self.eval()

    def eval_operation(self, sockets_input_data: list) -> list:
        sub_scene = self.get_sub_scene()
        if hasattr(sub_scene, 'inlets'):
            # sort sockets by vertical placement
            ordered_inlets = sorted(sub_scene.inlets, key=lambda inlet: inlet.pos.y(), reverse=True)
            for i, input_data in enumerate(sockets_input_data):
                ordered_inlets[i].setData(input_data)
                ordered_inlets[i].markDirty()
                ordered_inlets[i].eval()

        if hasattr(sub_scene, 'outlets'):
            ret = []
            for outlet in sorted(sub_scene.outlets, key=lambda outlet: outlet.pos.y(), reverse=True):
                outlet.markDirty()
                outlet.eval()
                ret.append(outlet.data)
            return ret
        return None

    def serialize(self):
        res = super().serialize()
        res['sub_scene'] = self.get_sub_scene().serialize()
        return res

    def deserialize(self, data: dict, hashmap=None, restore_id: bool = True):
        if hashmap is None:
            hashmap = {}
        res = super().deserialize(data, hashmap, restore_id)
        self.get_sub_scene().deserialize(data['sub_scene'])
        return res
