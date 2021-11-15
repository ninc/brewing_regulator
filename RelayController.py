#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging

from relay_lib_seeed import *

log = logging.getLogger(__name__)



class RelayController:
    """Base class that handles relay types"""
    _relayState = []
    _numberOfRelays = 4

    def __init__(self):
        # Initialize relay status
        for i in range(1, self._numberOfRelays + 1):
            self._relayState.append(relay_get_port_status(i))

    def getRelayState(self, relayNumber):
        self._relayState[relayNumber] = relay_get_port_status(relayNumber)
        return self._relayState[relayNumber]

    def setRelayOn(self, relayNumber):
        relay_on(relayNumber)

    def setRelayOff(self, relayNumber):
        relay_off(relayNumber)

    def setAllRelaysOff(self):
        for relayNumber in range(1, self._numberOfRelays+1):
            self.setRelayOff(relayNumber)

    def selfTest(self):
        # Cycle all relays on and off
        log.info('SelfTest started')
        for i in range(1, self._numberOfRelays + 1):
            self.setRelayOn(i)
            time.sleep(0.5)
            self.setRelayOff(i)
            time.sleep(0.5)


if __name__ == '__main__':
    try:
        logging.basicConfig(filename='/var/log/brewing_regulator.log', format='%(asctime)s %(levelname)-8s %(message)s', level=os.environ.get("LOGLEVEL", "INFO"))
        # Testing Relays
        rc = RelayController()
        rc.selfTest()
    except KeyboardInterrupt:
        log.error("Exiting application")
        relay_all_off()
        sys.exit(0)
