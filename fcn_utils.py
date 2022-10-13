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
from collections.abc import Iterable


def simplify(data_structure: list) -> list:
    """Flattens an iterable, but it leaves a minimal nesting. This is actual for vector sockets where one usually does
    not want to concatenate coordinates of different vectors into a big list.

    :param data_structure: Editor Scene in which the node is to be inserted.
    :type data_structure: list
    :return: Simplified list of sub lists
    :rtype: list
    """
    res: list = []

    copy: list = data_structure[:]
    while copy:
        entry: list = copy.pop()
        if isinstance(entry, Iterable):
            if len(entry) > 0 and not (isinstance(entry[0], Iterable)):
                res.append(entry)
            copy.extend(entry)

    res.reverse()
    return res


def traverse(nested_list):
    if isinstance(nested_list, list):
        for sub_list in nested_list:
            yield from traverse(sub_list)
    else:
        if isinstance(nested_list, tuple):
            yield nested_list
