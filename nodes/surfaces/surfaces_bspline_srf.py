# -*- coding: utf-8 -*-
###################################################################################
#
#  surfaces_bspline_surfaces.py
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
from FreeCAD import Vector
import Part

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import map_objects, map_last_level, broadcast_data_tree, ListWrapper

from nodes_locator import icon


@register_node
class BSplineSurface(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "BSpline Srf"
    op_category: str = "Surfaces"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Int Points", True)],
                         outputs_init_list=[("Face", True)])

        self.grNode.resize(120, 70)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    def eval_operation(self, sockets_input_data: list) -> list:
        # Get socket inputs
        point_input: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else \
            [[Vector(-5, 5, 5), Vector(0, 5, 0), Vector(5, 5, 5)],
             [Vector(-5, 0, 0), Vector(0, 0, 3), Vector(5, 0, 0)],
             [Vector(-5, -5, 5), Vector(0, -5, 0), Vector(5, -5, 5)]]

        # Calculate result
        bspline_surface: Part.BSplineSurface = Part.BSplineSurface()
        bspline_surface.interpolate(point_input)

        return [[bspline_surface]]
