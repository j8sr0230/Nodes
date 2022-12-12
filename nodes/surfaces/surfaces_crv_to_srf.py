# -*- coding: utf-8 -*-
###################################################################################
#
#  surfaces_crv_to_srf.py
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
from core.nodes_utils import map_objects, map_last_level, ListWrapper

from nodes_locator import icon


@register_node
class CrvToSurface(FCNNodeModel):

    icon: str = icon("nodes_crv_srf.svg")
    op_title: str = "Crv to Srf"
    op_category: str = "Surfaces"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Curve", True)],
                         outputs_init_list=[("Face", True)])

        self.grNode.resize(110, 70)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def make_face(curves_wrapper: ListWrapper) -> Part.Shape:
        wires: list = curves_wrapper.wrapped_data
        return Part.makeFace(wires, "Part::FaceMakerBullseye")

    def eval_operation(self, sockets_input_data: list) -> list:
        # Get socket inputs
        curve_input: list = [sockets_input_data[0]]

        # Needed, to treat list as atomic object during mapping
        wrapped_curve_input: list = list(map_last_level(curve_input, Part.Shape | Part.BSplineCurve | Part.Arc,
                                                        ListWrapper))

        # Calculate result
        faces = list(map_objects(wrapped_curve_input, ListWrapper, self.make_face))
        return [faces]
