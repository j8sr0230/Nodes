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
import FreeCAD as App
import FreeCADGui as Gui
import Part
from pivy import coin
import awkward as ak

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon
from fcn_utils import simplify, map_objects


@register_node
class Box(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Box"
    op_category: str = "Generator"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene: 'Scene'):
        self.width_list = []
        self.length_list = []
        self.height_list = []

        super().__init__(scene=scene,
                         inputs_init_list=[(0, "W", 1, 10, True, ("int", "float")),
                                           (0, "L", 1, 10, True, ("int", "float")),
                                           (0, "H", 1, 10, True, ("int", "float")),
                                           (1, "Pos", 0, 0, True, ("vec", ))],
                         outputs_init_list=[(3, "Box", 0, 0, True, ("shape", ))],
                         width=150)

    def make_coin_box(self, position: tuple):
        trans = coin.SoTranslation()
        trans.translation.setValue(position)

        box = coin.SoCube()
        box.width = self.width_list.pop(0)
        box.height = self.length_list.pop(0)
        box.depth = self.height_list.pop(0)

        sg_node = coin.SoSeparator()
        sg_node.addChild(trans)
        sg_node.addChild(box)

        return sg_node

    def make_occ_box(self, position: tuple):
        box = Part.makeBox(self.width_list.pop(0), self.length_list.pop(0), self.height_list.pop(0),
                           App.Vector(position))
        return box

    def eval_operation(self, sockets_input_data: list) -> list:
        width = sockets_input_data[0]
        length = sockets_input_data[1]
        height = sockets_input_data[2]
        pos = sockets_input_data[3] if len(sockets_input_data[3]) > 0 else [(0, 0, 0)]

        # Force array broadcast
        pos_list = simplify(pos)
        pos_idx_list = list(range(len(pos_list)))
        width, length, height, pos_idx_list = ak.broadcast_arrays(width, length, height, pos_idx_list)

        self.width_list = ak.flatten(width, axis=None).tolist()
        self.length_list = ak.flatten(length, axis=None).tolist()
        self.height_list = ak.flatten(height, axis=None).tolist()

        # return [map_objects(pos, tuple, self.make_coin_box)]
        return [map_objects(pos, tuple, self.make_occ_box)]
