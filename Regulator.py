#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging

log = logging.getLogger(__name__)

from RelayController import *
from TemperatureSensor import *

class Regulator:
    """Regulates the brewing process"""

    def __init__(self):
        self.rc = RelayController()
        self.ts = TemperatureSensor()
        self._heatingRelay = 1
        self._coolingRelay = 2

    def pid(self, targetTemp):
        currentTemp = self.ts.getFilteredTemperature()

        #TODO: Implement margin of error
        if currentTemp < targetTemp:
            #Turn on heating
            self.rc.setRelayOn(self._heatingRelay)
            self.rc.setRelayOff(self._coolingRelay)
            log.info('Too cold, turned on heating. Current Temperature {}c, Target Temperature {}c'.format(currentTemp, targetTemp))
        elif currentTemp > targetTemp:
            #Turn on cooling
            self.rc.setRelayOff(self._heatingRelay)
            self.rc.setRelayOn(self._coolingRelay)
            log.info('Too warm, turned on cooling. Current Temperature {}c, Target Temperature {}c'.format(currentTemp, targetTemp))
        else:
            # Within margin, do nothing
            self.rc.setRelayOff(self._heatingRelay)
            self.rc.setRelayOff(self._coolingRelay)
            log.info('Temperature within margins, doing nothing. Current Temperature {}c, Target Temperature {}c'.format(currentTemp, targetTemp))


    def selfTest(self):
        log.info('SelfTest started')
        self.rc.selfTest()
        self.ts.selfTest()


if __name__ == '__main__':
    try:
        logging.basicConfig(filename='/var/log/brewing_regulator.log', format='%(asctime)s %(levelname)-8s %(message)s', level=os.environ.get("LOGLEVEL", "INFO"))
        # Testing Relays
        regulator = Regulator()
        regulator.selfTest()
    except KeyboardInterrupt:
        log.error("Exiting application")
        sys.exit(0)
