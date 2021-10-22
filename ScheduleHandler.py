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
        self._activeSchedule = None
        self._activeStep = 0
        self.readActiveSchedule()

    def _splitScheduleValue(self, value):
        """Splits the schedule values into temperature and time"""
        #TODO: Replace with regexp
        tmp_str = value.split()
        temperature = tmp_str[0].replace('[', '').strip()
        t = tmp_str[1].replace(']', '').strip()
        return temperature, t

    def _validTemperature(self, temperature):
        """Verifies that the temperature format provided in the schedule is correct"""
        if 'c' not in temperature:
            return False
        
        #Verify that we can cast the input to a number
        try:
            float(temperature.replace('c', ''))
        except ValueError:
            return False
        return True

    def _validTime(self, t):
        """Verifies that the time format provided in the schedule is correct"""
        tmpTime = t
        if 'h' in t:
            tmpTime = t.replace('h', '')
        elif 'd' in t:
            tmpTime = t.replace('d', '')            
        else:
            return False
        
        #Verify that we can cast the input to a number
        try:
            float(tmpTime)
        except ValueError:
            return False

        return True

    def _verifyKeySequence(self, keys):
        """Verifies that all the keys are in a sequence"""
        keys.sort()
        i = keys[0]
        for key in keys:
            if i != key:
                log.error('Invalid stepping sequence, {} is missing in {}'.format(i, keys))
                return False
            i = i + 1
        return True

    def _verifySchedule(self, schedule):
        """Verifies the format of a schedule"""
        verified = True
        keys = []
        for each_section in schedule.sections():
            if each_section.lower() == 'activestep':
                    continue
            for each_key, each_val in schedule.items(each_section):
                temperature, t = self._splitScheduleValue(each_val)
                if not self._validTemperature(temperature):
                    log.error('Invalid time format in config {}={}'.format(each_key, each_val))
                    verified = False
                if not self._validTime(t):
                    log.error('Invalid temperature format in config {}={}'.format(each_key, each_val))
                    verified = False
                try:
                    keys.append(int(each_key))
                except ValueError:
                    verified = False

        if not self._verifyKeySequence(keys):
            verified = False
        return verified

    def setNewSchedule(self, schedule):
        log.info('New schedule selected {}'.format(schedule))
        newSchedule = configparser.ConfigParser()
        newSchedule.read(schedule)
        if self._verifySchedule(newSchedule):
            #Copy schedule to active folder
            self._activeSchedule = newSchedule
            self._activeStep = 1
            self._saveActiveSchedule()
        else:
            log.error('Failed to set new schedule due to previous errors')

    def _saveActiveSchedule(self):
        log.info('Saving new schedule to {}'.format(self._activeSchedulePath))

        if 'ActiveStep' not in self._activeSchedule.sections():
            self._activeSchedule.add_section('ActiveStep')
        self._activeSchedule.set('ActiveStep','step', str(self._activeStep))
        with open(self._activeSchedulePath, 'w') as configfile:
            self._activeSchedule.write(configfile)

    def readActiveSchedule(self):
        self._activeSchedule = configparser.ConfigParser()
        self._activeSchedule.read(self._activeSchedulePath)
        if not self._verifySchedule(self._activeSchedule):
            log.error('Failed to verify active schedule: {}'.format(self._activeSchedulePath))
        try:
            self._activeStep = int(self._activeSchedule['ActiveStep']['step'])
        except:
            # Default incase of corrupt settings file
            self._activeStep = 0

    def printActiveSchedule(self):
        """Prints the active schedule to stdout"""
        for each_section in self._activeSchedule.sections():
            print(each_section)
            for each_key, each_val in self._activeSchedule.items(each_section):
                print('{}={}'.format(each_key, each_val))

    def advanceSchedule(self):
        #TODO: When to end?
        self._activeStep = self._activeStep + 1
        log.info('Advancing schedule to step {}'.format(self._activeStep))
        self._saveActiveSchedule()

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
