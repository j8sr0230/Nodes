# -*- coding: utf-8 -*-
###################################################################################
#
#  fcn_utils.py
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


def flatten_to_vectors(data_structure: list) -> list:
    """Flattens a vector list of arbitrary depth to a simple list of 3D vectors.

    :param data_structure: Editor Scene in which the node is to be inserted.
    :type data_structure: list
    :return: Flat list of 3D vectors
    :rtype: list
    """
    res: list = []

    copy: list = data_structure[:]
    while copy:
        entry: list = copy.pop()
        if isinstance(entry, list):
            if len(entry) == 3 and all(isinstance(i, float) for i in entry):
                res.append(entry)
            copy.extend(entry)

    return res
