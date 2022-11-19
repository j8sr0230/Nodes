# -*- coding: utf-8 -*-
###################################################################################
#
#  spatial_populate_solid.py
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
import random

import numpy as np
import awkward as ak

from FreeCAD import Vector
import Part

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import flatten, map_objects

from nodes_locator import icon


DEBUG = True
BATCH_SIZE = 100
MAX_ITERATIONS = 1000


@register_node
class PopulateSolid(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Populate Solid"
    op_category: str = "Spatial"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Shape", True), ("Count", False), ("Distance", False), ("Seed", False)],
                         outputs_init_list=[("Point", True)])

        self.count: int = 10
        self.radius: float = 0
        self.seed: int = 0

        self.grNode.resize(130, 120)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

    ###################################################################################
    # Based on https://github.com/nortikin/sverchok/blob/master/utils/field/probe.py
    @staticmethod
    def check_min_radius(new_position: list, old_positions: list, min_radius: float) -> bool:
        if not old_positions:
            return True

        new_position: np.array = np.array(new_position)
        old_positions: np.array = np.array(old_positions)
        distances: np.array = np.linalg.norm(old_positions - new_position, axis=1)
        ok: bool = (min_radius < distances).all()

        return ok

    def populate_positions(self, solid: Part.Solid) -> list:
        box = solid.BoundBox
        bbox = ((box.XMin, box.YMin, box.ZMin), (box.XMax, box.YMax, box.ZMax))
        b1, b2 = bbox
        x_min, y_min, z_min = b1
        x_max, y_max, z_max = b2

        done: int = 0
        iterations: int = 0
        generated_positions: list = []

        while done < self.count:
            iterations += 1

            if DEBUG:
                print("Iteration no.:", iterations)

            if iterations > MAX_ITERATIONS:
                raise ValueError("Maximum number of iterations reached.", MAX_ITERATIONS)

            left: int = self.count - done
            batch_size: int = min(BATCH_SIZE, left)

            batch_x: list = list(np.random.uniform(low=x_min, high=x_max, size=batch_size))
            batch_y: list = list(np.random.uniform(low=y_min, high=y_max, size=batch_size))
            batch_z: list = list(np.random.uniform(low=z_min, high=z_max, size=batch_size))
            batch: list = list(zip(batch_x, batch_y, batch_z))

            candidates: list = [coordinate for coordinate in batch if solid.isInside(Vector(coordinate), 0.1, True)]

            if len(candidates) > 0:
                if self.radius == 0:
                    good_positions: list = candidates
                else:
                    good_positions: list = []
                    for candidate in candidates:
                        if self.check_min_radius(candidate, generated_positions + good_positions,
                                                 self.radius):
                            good_positions.append(candidate)

                generated_positions.extend(good_positions)
                done += len(good_positions)

        return [Vector(coordinates) for coordinates in generated_positions]
    ###################################################################################

    def eval_operation(self, sockets_input_data: list) -> list:
        solid: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [None]
        self.count: int = int(sockets_input_data[1][0]) if len(sockets_input_data[1]) > 0 else 10
        self.radius: float = float(sockets_input_data[2][0]) if len(sockets_input_data[2]) > 0 else 0
        self.seed: int = int(sockets_input_data[3][0]) if len(sockets_input_data[3]) > 0 else 0

        np.random.seed(self.seed)

        return [map_objects(solid, Part.Solid, self.populate_positions)]
