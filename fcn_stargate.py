# -*- coding: utf-8 -*-
###################################################################################
#
#  stargate.py
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

TELEPORTER_FREE_ID=1

class _Stargate:
    knownTeleporters: dict = {}

    def addTeleporter(self, input=None, output=None):
        global TELEPORTER_FREE_ID
        tele_id = TELEPORTER_FREE_ID
        TELEPORTER_FREE_ID += 1
        teleporter = Teleporter(input, output, tele_id)
        self.knownTeleporters[tele_id] = teleporter
        return tele_id

    def renameTeleporter(self, old_id, new_id):
        try:
            self.knownTeleporters[new_id] = self.knownTeleporters[old_id]
            return True
        except:
            return False

    def getTeleporter(self, tele_id):
        try:
            return self.knownTeleporters[tele_id]
        except:
            return False

    def removeTeleporter(self, tele_id):
        try:
            del self.knownTeleporters[tele_id]
            return True
        except:
            return False

stargate = _Stargate()

class Teleporter:
    def __init__(self, input, output, id):
        self.input = input
        self.output = output
        self.id = id

    def setInput(self, input):
        self.input = input
        self.checkValidity()

    def setOutput(self, output):
        self.output = output
        self.checkValidity()

    def checkValidity(self):
        # remove teleporter w/o input nor output
        if self.input is None and self.output is None:
            stargate.removeTeleporter(self.id)
