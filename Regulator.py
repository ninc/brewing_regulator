#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import logging

log = logging.getLogger(__name__)

from RelayController import *
from TemperatureSensor import *

class Regulator:
    """Regulates the brewing process"""

    def __init__(self, targetTemp):
        self._targetTemperature = targetTemp
        self.rc = RelayController()
        self.ts = TemperatureSensor()
        self._heatingRelay = 1
        self._coolingRelay = 2

    def pid(self):
        #TODO: Implement this
        currentTemp = self.ts.getFilteredTemperature()

        #TODO: Implement margin of error
        if currentTemp < self._targetTemperature:
            #Turn on heating
            self.rc.setRelayOn(self._heatingRelay)
            self.rc.setRelayOff(self._coolingRelay)
            log.info('Too cold, turned on heating. Current Temperature {}c, Target Temperature {}c'.format(currentTemp, self._targetTemperature))
        elif currentTemp > self._targetTemperature:
            #Turn on cooling
            self.rc.setRelayOff(self._heatingRelay)
            self.rc.setRelayOn(self._coolingRelay)
            log.info('Too warm, turned on cooling. Current Temperature {}c, Target Temperature {}c'.format(currentTemp, self._targetTemperature))
        else:
            # Within margin, do nothing
            self.rc.setRelayOff(self._heatingRelay)
            self.rc.setRelayOff(self._coolingRelay)
            log.info('Temperature within margins, doing nothing. Current Temperature {}c, Target Temperature {}c'.format(currentTemp, self._targetTemperature))


    def selfTest(self):
        log.info('SelfTest started')
        self.rc.selfTest()
        self.ts.selfTest()


if __name__ == '__main__':
    try:
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=os.environ.get("LOGLEVEL", "INFO"))
        # Testing Relays
        regulator = Regulator()
        regulator.selfTest()
    except KeyboardInterrupt:
        log.error("Exiting application")
        sys.exit(0)
