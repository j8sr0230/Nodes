# -*- coding: utf-8 -*-
###################################################################################
#
#  nodes_locator.py
#
#  Copyright (c) 2021 Florian Foinant-Willig <ffw@2f2v.fr>
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

import os
import FreeCADGui

PATH = os.path.dirname(__file__)
RESOURCES_PATH = os.path.join(PATH, 'resources')
ICONS_PATH = os.path.join(PATH, 'icons')
TRANSLATIONS_PATH = os.path.join(PATH, 'translations')
NODES_PATH = os.path.join(PATH, 'nodes')


def icon(filename):
    return os.path.join(ICONS_PATH, filename)


def resource(filename):
    return os.path.join(RESOURCES_PATH, filename)


def getNodesWorkbench():
    return FreeCADGui.getWorkbench('NodesWorkbench')
