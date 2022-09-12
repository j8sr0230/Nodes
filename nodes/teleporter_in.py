# -*- coding: utf-8 -*-
###################################################################################
#
#  teleporter_in.py
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
class TeleporterInNode(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Teleporter In"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        self.id = stargate.addTeleporter(input=self)

        super().__init__(scene=scene,
                         inputs_init_list=[(0, "Id", 1, self.id, False), (0, "In", 0, 0, True)],
                         outputs_init_list=[(0, "Id", 0, self.id, True)],
                         width=250)

    def collapse_node(self, collapse: bool = False):
        super().collapse_node(collapse)
        if collapse is True:
            self.title = self.default_title + f' <{self.id}>'
        else:
            self.title = self.default_title

    def eval_operation(self, sockets_input_data: list) -> list:
        tele_id = sockets_input_data[0][0]

        teleporter = stargate.getTeleporter(self.id)
        if tele_id != self.id:
            new_tele = stargate.getTeleporter(tele_id)
            if new_tele:
                new_tele.setInput(self)
                if teleporter:
                    teleporter.setInput(None)
                teleporter = new_tele
            else:
                stargate.renameTeleporter(self.id, tele_id)
            self.id = tele_id

        if teleporter and teleporter.output is not None:
            # force recompute at second extremity
            teleporter.output.setData(sockets_input_data[1])
            teleporter.output.markInvalid()
            teleporter.output.eval()

        return [self.id]
