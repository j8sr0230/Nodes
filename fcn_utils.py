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
import awkward as ak


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


def nest_items(template, items):
    """Generates a template-defined nested list of items.

    This function creates a list with the nested structure of the template list. The following rules apply to the
    elements of this new nested list:
    - Tuples within the template list are chronologically replaced by elements from the item list.
    - All other non-iterable data types are replaced by a 'None' as marker.

    :param template: Template list, with the desired nested structure (may contain tuples).
    :type template: list
    :param items: Flat list (stack) of items, to replace tuples.
    :type items: list
    :return: New nested list with the template-defined list structure and items instead of tuples.
    :rtype: list
    """

    items_copy = items[:]

    if isinstance(template, list):
        temp_list = []
        for sub_list in template:
            temp_list.append(nest_items(sub_list, items))
        return temp_list
    else:
        if isinstance(template, tuple):
            return items_copy.pop(0)
