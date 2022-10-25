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
from pivy import coin
import awkward as ak

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon
from fcn_utils import flatten


@register_node
class CompoundViewer(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Compound Viewer"
    op_category = "Viz"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        if hasattr(Gui, "ActiveDocument"):
            self.fc_obj = App.ActiveDocument.addObject("Part::Feature", "Viewer")
            self.fc_obj.setPropertyStatus("Shape", ["Transient", "Output"])

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
        shapes = flatten(sockets_input_data[0])

        if hasattr(Gui, "ActiveDocument"):
            if len(shapes) > 0:
                comp = Part.makeCompound(shapes)
                self.fc_obj.Shape = comp
                App.activeDocument().recompute()

        return [sockets_input_data[0]]
