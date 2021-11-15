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
        self._marginOfError = 0.5 # Margin of 0.5 celsius

    def pid(self, targetTemp):
        currentTemp = self.ts.getFilteredTemperature()
        log.info('Current Temperature {}c, Target Temperature {}c, Margin {}c'.format(currentTemp, targetTemp, self._marginOfError))
        print('Current Temperature {}c, Target Temperature {}c, Margin {}c'.format(currentTemp, targetTemp, self._marginOfError))
        if currentTemp < targetTemp - self._marginOfError:
            #Turn on heating
            self.rc.setRelayOn(self._heatingRelay)
            self.rc.setRelayOff(self._coolingRelay)
            log.info('Too cold, turned on heating.')
            print('Too cold, turned on heating.')
        elif currentTemp > targetTemp + self._marginOfError:
            #Turn on cooling
            sleepTime = 5 #Minutes
            self.rc.setRelayOff(self._heatingRelay)
            self.rc.setRelayOn(self._coolingRelay)
            log.info('Too warm, turned on cooling. Sleeping for {}min.'.format(sleepTime))
            print('Too warm, turned on cooling. Sleeping for {}min.'.format(sleepTime))
            time.sleep(60*sleepTime)
        else:
            # Within margin, do nothing
            self.rc.setRelayOff(self._heatingRelay)
            self.rc.setRelayOff(self._coolingRelay)
            log.info('Temperature within margins, doing nothing.')
            print('Temperature within margins, doing nothing.')


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
