# -*- coding: utf-8 -*-
###################################################################################
#
#  group_send_receive.py
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
from blinker import signal

from core.nodes_conf import register_node
from core.nodes_base_node import FCNNode
from nodes_locator import icon


@register_node
class Sender(FCNNode):
    icon: str = icon("nodes_default.png")
    op_title: str = "Sender"
    op_category: str = "Group"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        self.data: list = []
        self.signal_id: str = ""
        self.push_data_signal: signal = None
        self.pull_data_signal: signal = signal("pull")

        super().__init__(scene=scene,
                         inputs_init_list=[(3, "Id", 1, "1", False, ('str', )), (6, "In", 0, 0, True, ('*', ))],
                         outputs_init_list=[(3, "Id", 0, "1", True, ('str', )), (6, "Out", 0, 0, True, ('*', ))],
                         width=150)

        self.pull_data_signal.connect(self.on_pull)

    def on_pull(self, sender):
        try:
            self.markDirty()
            self.eval()
        except Exception as e:
            print(e, sender)

    def collapse_node(self, collapse: bool = False):
        super().collapse_node(collapse)
        if collapse is True:
            input_value = self.sockets_input_data[0][0]
            self.title = 'Sender: ' + str(input_value)
        else:
            self.title = self.default_title

    def eval_operation(self, sockets_input_data: list) -> list:
        self.collapse_node(self.content.isHidden())

        signal_id = str(sockets_input_data[0][0])
        input_data = sockets_input_data[1]

        if self.signal_id != signal_id:
            # New sender signale id
            self.push_data_signal = signal(signal_id)
            self.signal_id = signal_id

        self.data = input_data
        self.push_data_signal.send(input_data)
        return [[signal_id], input_data]


@register_node
class Receiver(FCNNode):
    data: list
    icon: str = icon("nodes_default.png")
    op_title: str = "Receiver"
    op_category: str = "Group"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        self.data: list = []
        self.signal_id: str = ""
        self.push_data_signal: signal = None
        self.pull_data_signal: signal = signal("pull")

        super().__init__(scene=scene,
                         inputs_init_list=[(3, "Id", 1, "1", False, ('str', ))],
                         outputs_init_list=[(3, "Id", 0, "1", True, ('str', )), (6, "Out", 0, 0, True, ('*', ))],
                         width=150)

    def collapse_node(self, collapse: bool = False):
        super().collapse_node(collapse)
        if collapse is True:
            input_value = self.sockets_input_data[0][0]
            self.title = 'Receiver: ' + str(input_value)
        else:
            self.title = self.default_title

    def on_push(self, data):
        try:
            self.data = data
            self.markDirty()
            self.eval()
        except Exception as e:
            print(e, data)

    def eval_operation(self, sockets_input_data: list) -> list:
        self.collapse_node(self.content.isHidden())

        signal_id = str(sockets_input_data[0][0])

        if self.signal_id != signal_id:
            # New receiver signale id
            if hasattr(self.push_data_signal, "disconnect"):
                self.push_data_signal.disconnect(self.on_push)
                self.push_data_signal = None
            self.push_data_signal = signal(signal_id)
            self.signal_id = signal_id
            self.push_data_signal.connect(self.on_push)
            self.pull_data_signal.send(self)

        return [[signal_id], self.data if self.data else [0]]
