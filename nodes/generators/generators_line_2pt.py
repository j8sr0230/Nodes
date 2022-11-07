# -*- coding: utf-8 -*-
###################################################################################
#
#  generators_line_2pt.py
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
import awkward as ak

from FreeCAD import Vector
import Part

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import flatten, map_objects

from nodes_locator import icon


@register_node
class Line2Pt(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Line (2Pt)"
    op_category: str = "Generators"
    content_label_objname: str = "fcn_node_bg"

    start_flat: list
    end_flat: list
    end_idx: list

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Start", True), ("End", True)],
                         outputs_init_list=[("Line", True)])

        self.grNode.resize(100, 80)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def make_occ_line(self, start_idx: int) -> Part.Shape:
        try:
            return Part.makeLine(self.start_flat[start_idx], self.end_flat[self.end_idx.pop(0)])
        except Part.OCCError as e:
            raise(ValueError(e))

    def eval_operation(self, sockets_input_data: list) -> list:
        start: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [Vector(0, 0, 0)]
        self.start_flat = list(flatten(start))

        end: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [Vector(10, 0, 0)]
        self.end_flat = list(flatten(end))

        # Force array broadcast
        start_idx_nested = map_objects(start, Vector, lambda vec: self.start_flat.index(vec))
        end_idx_flat = list(range(len(self.end_flat)))

        start_idx, end_idx = ak.broadcast_arrays(start_idx_nested, end_idx_flat)
        self.end_idx = ak.flatten(end_idx, axis=None).tolist()

        return [map_objects(start_idx.tolist(), int, self.make_occ_line)]
