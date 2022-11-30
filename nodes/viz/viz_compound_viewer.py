# -*- coding: utf-8 -*-
###################################################################################
#
#  viz_compound_viewer.py
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
import Part

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import flatten

from nodes_locator import icon


@register_node
class CompoundViewer(FCNNodeModel):

    icon: str = icon("nodes_cview.svg")
    op_title: str = "CViewer"
    op_category: str = "Viz"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        if hasattr(Gui, "ActiveDocument"):
            self.fc_obj = App.ActiveDocument.addObject("Part::Feature", "CViewer")
            self.fc_obj.setPropertyStatus("Shape", ["Transient", "Output"])

        super().__init__(scene=scene, inputs_init_list=[("In", True)], outputs_init_list=[])

    def remove(self):
        super().remove()

        if hasattr(Gui, "ActiveDocument"):
            if self.fc_obj is not None:
                App.ActiveDocument.removeObject(self.fc_obj.Name)

    def eval_operation(self, sockets_input_data: list) -> list:
        shapes = list(flatten(sockets_input_data[0]))

        if hasattr(Gui, "ActiveDocument"):
            if len(shapes) > 0:
                comp = Part.makeCompound(shapes)
                self.fc_obj.Shape = comp
                App.activeDocument().recompute()

        return [sockets_input_data[0]]
