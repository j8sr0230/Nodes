# -*- coding: utf-8 -*-
###################################################################################
#
#  teleporter_out.py
#
#  Copyright (c) 2022 Florian Foinant-Willig <ffw@2f2v.fr>
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

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon
from fcn_stargate import stargate


@register_node
class TeleporterOutNode(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Teleporter Out"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        self.id = stargate.addTeleporter(output=self)
        self.data = [0]
        super().__init__(scene=scene,
                         inputs_init_list=[(0, "Id", 1, self.id, False)],
                         outputs_init_list=[(0, "Id", 0, self.id, True), (0, "Out", 0, 0, True)],
                         width=150)

    def collapse_node(self, collapse: bool = False):
        super().collapse_node(collapse)
        if collapse is True:
            self.title = self.default_title + f' <{self.id}>'
        else:
            self.title = self.default_title

    def setData(self, data):
        self.data = data

    def eval_operation(self, sockets_input_data: list) -> list:
        tele_id = sockets_input_data[0][0]

        if tele_id != self.id:
            teleporter = stargate.getTeleporter(self.id)
            new_tele = stargate.getTeleporter(tele_id)
            if new_tele:
                new_tele.setOutput(self)
                if teleporter:
                    teleporter.setOutput(None)
                teleporter = new_tele
            else:
                stargate.renameTeleporter(self.id, tele_id)
            self.id = tele_id

        return [[self.id], self.data]
