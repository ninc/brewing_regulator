#!/usr/bin/env python
# -*- coding: utf-8 -*-


class RelayController:
"""Base class that handles relay types"""
    currentRelayState = False

    def __init__(self):
        pass

    def getRelayState(self):
        pass

    def setRelayState(self):
        pass