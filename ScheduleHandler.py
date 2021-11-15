#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import sys
import configparser
from datetime import datetime, timedelta


this_path = os.path.dirname(os.path.realpath(__file__))
log = logging.getLogger(__name__)

class ScheduleHandler:
    """Handles the Brewing Schedule"""

    def __init__(self):
        self._activeSchedulePath = '{}/active_schedule/active_schedule.ini'.format(this_path)
        self._activeSchedule = None
        self._currentStepTime = None
        self._currentStep = 1
        self._lastStep = None
        self._brewingDone = False
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
        elif 'm' in t:
            tmpTime = t.replace('m', '')          
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
        self.keys = []
        self.temperatures = []
        self.timers = []
        for each_section in schedule.sections():
            if each_section.lower() == 'currentbrew':
                    continue
            for each_key, each_val in schedule.items(each_section):
                temperature, t = self._splitScheduleValue(each_val)
                if not self._validTemperature(temperature):
                    log.error('Invalid temperature format in config {}={}'.format(each_key, each_val))
                    verified = False
                if not self._validTime(t):
                    log.error('Invalid time format in config {}={}'.format(each_key, each_val))
                    verified = False
                try:
                    self.keys.append(int(each_key))
                except ValueError:
                    verified = False
                self.temperatures.append(temperature)
                self.timers.append(t)
        if not self._verifyKeySequence(self.keys):
            verified = False
        return verified

    def setNewSchedule(self, schedule):
        log.info('New schedule selected {}'.format(schedule))
        newSchedule = configparser.ConfigParser()
        newSchedule.read(schedule)
        if self._verifySchedule(newSchedule):
            #Copy schedule to active folder
            self._activeSchedule = newSchedule
            self._currentStep = 1
            self._brewStartTime = datetime.now()
            self._saveActiveSchedule()
        else:
            log.error('Failed to set new schedule due to previous errors')

    def _saveActiveSchedule(self):
        # If the schedule is brand new
        if 'CurrentBrew' not in self._activeSchedule.sections():
            self._activeSchedule.add_section('CurrentBrew')
            self._activeSchedule.set('CurrentBrew','BrewStartTime', str(self._brewStartTime))
            # Add timers and temperatures to active schedule for easier handling
            for i in range(0, len(self.keys)):
                self._activeSchedule.set('CurrentBrew', 'Temp{}'.format(self.keys[i]), self._calcTemp(i))
                self._activeSchedule.set('CurrentBrew', 'Timer{}'.format(self.keys[i]), self._calcTime(i))

        # Update current step
        self._activeSchedule.set('CurrentBrew','CurrentStep', str(self._currentStep))

        with open(self._activeSchedulePath, 'w') as configfile:
            self._activeSchedule.write(configfile)

    def _calcTemp(self, index):
        temp = self.temperatures[index]
        return temp.replace('c', '')

    def _calcTime(self, index):
        # Use _currentStepTime to remember the previous iterations
        if self._currentStepTime == None:
            self._currentStepTime = self._brewStartTime

        t = self.timers[index]
        if 'h' in t:
            time_float = float(t.replace('h', ''))
            self._currentStepTime = self._currentStepTime + timedelta(hours=time_float)
        elif 'd' in t:
            time_float = float(t.replace('d', ''))
            self._currentStepTime = self._currentStepTime + timedelta(days=time_float)
        elif 'm' in t:
            time_float = float(t.replace('m', ''))
            self._currentStepTime = self._currentStepTime + timedelta(minutes=time_float)
        return str(self._currentStepTime)

    def readActiveSchedule(self):
        self._activeSchedule = configparser.ConfigParser()
        self._activeSchedule.read(self._activeSchedulePath)
        if not self._verifySchedule(self._activeSchedule):
            log.error('Failed to verify active schedule: {}'.format(self._activeSchedulePath))
        try:
            self._activeStep = int(self._activeSchedule['CurrentBrew']['CurrentStep'])
            self._brewStartTime = datetime.strptime(self._activeSchedule['CurrentBrew']['BrewStartTime'], '%Y-%m-%d %H:%M:%S.%f')
            self._lastStep = len(self.keys)
        except:
            # Default incase of corrupt settings file
            self._activeStep = 0

    def printActiveSchedule(self):
        """Prints the active schedule to stdout"""
        for each_section in self._activeSchedule.sections():
            print(each_section)
            for each_key, each_val in self._activeSchedule.items(each_section):
                print('{}={}'.format(each_key, each_val))

    def getTargetTemperature(self):
        if self._activeStep == 0:
            return None
        else:
            schedule_value = self._activeSchedule['Schedule'][str(self._activeStep)]
            temperature, t = self._splitScheduleValue(schedule_value)
            targetTemp = float(temperature.replace('c', ''))
            return targetTemp

    def getCurrentStep(self):
        self._currentStep = int(self._activeSchedule['CurrentBrew']['currentstep'])

    def getNextScheduleTimer(self):
        self.getCurrentStep()
        timer = 'timer{}'.format(self._currentStep)
        nextTimer = datetime.strptime(self._activeSchedule['CurrentBrew'][timer], '%Y-%m-%d %H:%M:%S.%f')
        return nextTimer

    def advanceSchedule(self):
        currentTime = datetime.now()
        nextTimer = self.getNextScheduleTimer()

        # Advance schedule if needed
        if nextTimer < currentTime:
            self._currentStep = self._currentStep + 1
            log.info('Advancing schedule to step {}'.format(self._currentStep))
            self._saveActiveSchedule()

    def brewingDone(self):
        self.getCurrentStep()
        if self._currentStep > self._lastStep:
            self._brewingDone = True
        return self._brewingDone

    def getBrewStartTime(self):
        brewStartTime = self._activeSchedule['CurrentBrew']['BrewStartTime']
        return brewStartTime

    def selfTest(self):
        test_schedule = 'test/test_schedule.ini'
        self.setNewSchedule(test_schedule)
        self.readActiveSchedule()
        self.printActiveSchedule()

if __name__ == '__main__':
    try:
        logging.basicConfig(filename='/var/log/brewing_regulator.log', format='%(asctime)s %(levelname)-8s %(message)s', level=os.environ.get("LOGLEVEL", "INFO"))
        sh = ScheduleHandler()
        sh.selfTest()
    except KeyboardInterrupt:
        log.error("Exiting application")
        sys.exit(0)
