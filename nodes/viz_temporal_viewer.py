# -*- coding: utf-8 -*-
###################################################################################
#
#  viz_temporal_viewer.py
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
import FreeCADGui as Gui
from pivy import coin
import awkward as ak

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon
from fcn_utils import flatten


@register_node
class TemporalViewer(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Temporal Viewer"
    op_category = "Viz"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        self.sg_nodes = []

        super().__init__(scene=scene,
                         inputs_init_list=[(3, "In", 0, 0, True, ("shape", )),
                                           (0, "R", 2, (0, 255, 255), False, ("int", )),
                                           (0, "G", 2, (0, 255, 0), False, ("int", )),
                                           (0, "B", 2, (0, 255, 0), False, ("int", ))],
                         outputs_init_list=[(3, "Out", 0, 0, True, ("shape", ))],
                         width=170)

    def remove(self):
        super().remove()

        if hasattr(Gui, "ActiveDocument"):
            view = Gui.ActiveDocument.ActiveView
            sg = view.getSceneGraph()
            for sg_node in self.sg_nodes:
                sg.removeChild(sg_node)

    def eval_operation(self, sockets_input_data: list) -> list:
        sg_nodes = flatten(sockets_input_data[0])
        rgb = (sockets_input_data[1][0]/255, sockets_input_data[2][0]/255, sockets_input_data[3][0]/255)

        color = coin.SoMaterial()
        color.diffuseColor = rgb

        if hasattr(Gui, "ActiveDocument"):
            view = Gui.ActiveDocument.ActiveView
            sg = view.getSceneGraph()

            if len(self.sg_nodes) > 0:
                for sg_node in self.sg_nodes:
                    sg.removeChild(sg_node)
                self.sg_nodes = []

            for sg_node in sg_nodes:
                sg_sep = coin.SoSeparator()
                sg_sep.addChild(color)
                sg_sep.addChild(sg_node)

                self.sg_nodes.append(sg_sep)
                sg.addChild(sg_sep)

        return [sockets_input_data[0]]
