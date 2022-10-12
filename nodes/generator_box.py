# -*- coding: utf-8 -*-
###################################################################################
#
#  generator_box.py
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
import numpy as np

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon
from fcn_utils import simplify


@register_node
class Box(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Box"
    op_category = "Generator"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        self.sg_nodes = []

        super().__init__(scene=scene,
                         inputs_init_list=[(0, "W", 1, 10, True, ("int", "float")),
                                           (0, "L", 1, 10, True, ("int", "float")),
                                           (0, "H", 1, 10, True, ("int", "float")),
                                           (1, "Pos", 0, 0, True, ("vec", ))],
                         outputs_init_list=[(3, "Box", 0, 0, True, ("shape", ))],
                         width=150)

    def remove(self):
        super().remove()

        if hasattr(Gui, "ActiveDocument"):
            view = Gui.ActiveDocument.ActiveView
            sg = view.getSceneGraph()
            for sg_node in self.sg_nodes:
                sg.removeChild(sg_node)

    def eval_operation(self, sockets_input_data: list) -> list:
        width = sockets_input_data[0]
        length = sockets_input_data[1]
        height = sockets_input_data[2]
        pos = sockets_input_data[3] if len(sockets_input_data[3]) > 0 else [(0, 0, 0)]
        pos = simplify(pos)

        # Force array broadcast
        pos_idx = np.arange(0, len(pos), 1)
        width, length, height, pos_idx = ak.broadcast_arrays(width, length, height, pos_idx)

        width_list = ak.flatten(width, axis=None).tolist()
        length_list = ak.flatten(length, axis=None).tolist()
        height_list = ak.flatten(height, axis=None).tolist()

        if hasattr(Gui, "ActiveDocument"):
            view = Gui.ActiveDocument.ActiveView
            sg = view.getSceneGraph()

            if len(self.sg_nodes) > 0:
                for sg_node in self.sg_nodes:
                    sg.removeChild(sg_node)
                self.sg_nodes = []

            for idx, _width in enumerate(width_list):
                box = coin.SoCube()
                box.width = _width
                box.height = length_list[idx]
                box.depth = height_list[idx]

                color = coin.SoMaterial()
                color.diffuseColor = (1., 0, 0)

                trans = coin.SoTranslation()
                trans.translation.setValue(pos[pos_idx[idx]])

                sg_node = coin.SoSeparator()
                sg_node.addChild(color)
                sg_node.addChild(trans)
                sg_node.addChild(box)

                self.sg_nodes.append(sg_node)
                sg.addChild(sg_node)

        return [[self.sg_nodes]]
