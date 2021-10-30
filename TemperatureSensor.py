#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import sys
import glob
import time
from statistics import mean

log = logging.getLogger(__name__)

class TemperatureSensor:
    """Base class that handles all temperature sensors"""

    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        # Find w1 device
        self.base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'

        # Read initial values to avoid errors
        self.readTemperature()


    def getFilteredTemperature(self):
        """Sample the sensor n times and create a moving average"""
        """Source: https://hackaday.com/2019/09/06/sensor-filters-for-coders/"""
        n = 10
        sensorValues = []
        for i in range(1, n):
            temp_c, _ = self.readTemperature()
            sensorValues.append(temp_c)

        return round(mean(sensorValues), 2) # Moving Average and round to 2 decimal points


    def _readTemperatureRaw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def readTemperature(self):
        # Taken from https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/
        lines = self._readTemperatureRaw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._readTemperatureRaw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f

    def selfTest(self):
        # Read the temperature sensor 10 times
        log.info('SelfTest started')
        for i in range(1, 10):
            temperature, _ = self.readTemperature()
            log.info('Temperature reading {}, {} Celsuis'.format(i, temperature))
            time.sleep(1)

if __name__ == '__main__':
    try:
        logging.basicConfig(filename='/var/log/brewing_regulator.log', format='%(asctime)s %(levelname)-8s %(message)s', level=os.environ.get("LOGLEVEL", "INFO"))
        # Testing Temperature Sensor
        ts = TemperatureSensor()
        ts.selfTest()
    except KeyboardInterrupt:
        log.error("Exiting application")
        sys.exit(0)