#!/usr/bin/env python
# -*- coding: utf-8 -*-


from seeed_studio_relay_board.relay_lib_seeed import *

class RelayController:
    """Base class that handles relay types"""
    currentRelayState = False

    def __init__(self):
        pass

    def getRelayState(self):
        pass

    def setRelayState(self):
        pass


if __name__ == '__main__':
    # Testing Relays
    rc = RelayController()