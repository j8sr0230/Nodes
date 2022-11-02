# -*- coding: utf-8 -*-
###################################################################################
#
#  viz_mesh_viewer.py
#
#  Copyright (c) 2022 Ronny Scharf-Wildenhain <ronny.scharf08@gmail.com>
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
import FreeCAD as App
import FreeCADGui as Gui
import Mesh

from editor.nodes_conf import register_node
from editor.nodes_base_node import FCNNode
from nodes_locator import icon
from editor.nodes_utils import flatten


@register_node
class CompoundViewer(FCNNode):

    icon: str = icon("nodes_default.png")
    op_title: str = "Mesh Viewer"
    op_category: str = "Viz"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        if hasattr(Gui, "ActiveDocument"):
            self.fc_obj = App.ActiveDocument.addObject("Mesh::Feature", "MViewer")

        super().__init__(scene=scene,
                         inputs_init_list=[(3, "In", 0, 0, True, ("shape", ))],
                         outputs_init_list=[(3, "Out", 0, 0, True, ("shape", ))],
                         width=170)

    def remove(self):
        super().remove()

        if hasattr(Gui, "ActiveDocument"):
            if self.fc_obj is not None:
                App.ActiveDocument.removeObject(self.fc_obj.Name)

    def eval_operation(self, sockets_input_data: list) -> list:
        meshes = flatten(sockets_input_data[0])

        if hasattr(Gui, "ActiveDocument"):
            if len(list(meshes)) > 0:

                merge = Mesh.Mesh()
                for mesh in meshes:
                    merge.addMesh(mesh)

                self.fc_obj.Mesh = merge
                App.activeDocument().recompute()

        return [sockets_input_data[0]]
