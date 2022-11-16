# -*- coding: utf-8 -*-
###################################################################################
#
#  spatial_voronoi_on_srf.py
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
import numpy as np
from scipy.spatial import Voronoi

from FreeCAD import Vector
import Part

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import map_objects

from nodes_locator import icon


@register_node
class VoronoiOnSrf(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Voronoi on Srf"
    op_category: str = "Spatial"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Face", True), ("Point", True), ("Scale", False)],
                         outputs_init_list=[("Wire", True)])

        self.scale: float = 1

        self.grNode.resize(130, 100)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    @staticmethod
    def make_voronoi(face: Part.Face) -> Part.Shape:
        return face

    def eval_operation(self, sockets_input_data: list) -> list:
        face: list = sockets_input_data[0]
        point: list = sockets_input_data[1]
        self.scale: float = float(sockets_input_data[1][0]) if len(sockets_input_data[1]) > 0 else 1

        return [map_objects(face, Part.Face, self.make_voronoi)]
