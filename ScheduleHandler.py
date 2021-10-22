#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
import configparser


log = logging.getLogger(__name__)

class ScheduleHandler:
    """Handles the Brewing Schedule"""

    def __init__(self):
        self._activeSchedulePath = 'active_schedule/active_schedule.ini'
        self.active_config = None
        self.readActiveSchedule()

    def setNewSchedule(self, schedule):
        log.info('New schdule selected {}'.format(schedule))
        new_config = configparser.ConfigParser()
        new_config.read(schedule)

    def readActiveSchedule(self):
        log.info('Parsing schedule {}'.format(self._activeSchedulePath))
        self.active_config = configparser.ConfigParser()
        self.active_config.read(self._activeSchedulePath)
        self.verifySchedule(self._activeSchedulePath)

    def _splitScheduleValue(self, value):
        """Splits the schedule values into temperature and time"""
        #TODO: Replace with regexp
        tmp_str = value.split()
        temperature = tmp_str[0].replace('[', '').strip()
        t = tmp_str[1].replace(']', '').strip()
        return temperature, t

    def validTemperature(self, temperature):
        """Verifies that the temperature format provided in the schedule is correct"""
        if 'c' not in temperature:
            return False
        
        #Verify that we can cast the input to a number
        try:
            float(temperature.replace('c', '')) 
        except ValueError:
            return False
        return True

    def validTime(self, t):
        """Verifies that the time format provided in the schedule is correct"""
        temp_time = t
        if 'h' in t:
            temp_time = t.replace('h', '')
        elif 'd' in t:
            temp_time = t.replace('d', '')            
        else:
            return False
        
        #Verify that we can cast the input to a number
        try:
            float(temp_time)
        except ValueError:
            return False

        return True

    def verifySchedule(self, schedule):
        """Verifies the format of a schedule"""
        log.info('Verifying schedule {}'.format(schedule))

        config = configparser.ConfigParser()
        config.read(schedule)

        #Will be set to false if anything fails
        verified = True

        for each_section in config.sections():
            for each_key, each_val in config.items(each_section):
                temperature, t = self._splitScheduleValue(each_val)
                if not self.validTemperature(temperature):
                    log.error('Invalid time format in config {}={}'.format(each_key, each_val))
                    verified = False
                if not self.validTime(t):
                    log.error('Invalid temperature format in config {}={}'.format(each_key, each_val))
                    verified = False

        return verified

    def printActiveSchedule(self):
        """Prints the active schedule to stdout"""
        for each_section in self.active_config.sections():
            print(each_section)
            for each_key, each_val in self.active_config.items(each_section):
                print('{}={}'.format(each_key, each_val))

    def selfTest(self):
        test_schedule = 'test/test_schedule.ini'
        self.setNewSchedule(test_schedule)
        self.readActiveSchedule()
        self.printActiveSchedule()

if __name__ == '__main__':
    try:
        logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
        sh = ScheduleHandler()
        sh.selfTest()
    except KeyboardInterrupt:
        log.error("Exiting application")
        sys.exit(0)