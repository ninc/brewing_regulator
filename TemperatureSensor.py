#!/usr/bin/env python
# -*- coding: utf-8 -*-

class TemperatureSensor:
"""Base class that handles all temperature sensors"""
    currentTemperature = 0.0 # Celsius

    def __init__(self):
        pass

    def getTemperature(self):
        pass

    def readTemperature(self):
        """Reads the temeperature sensor"""
        pass

    def inputFilter(self):
        """Filters the sensor values"""
        pass