#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import os
import argparse
import subprocess
import time
from datetime import datetime

from RelayController import *
from ScheduleHandler import *
from Regulator import *

log = logging.getLogger(__name__)
logging.basicConfig(filename='/var/log/brewing_regulator.log', format='%(asctime)s %(levelname)-8s %(message)s', level=os.environ.get("LOGLEVEL", "INFO"))

def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

class BrewingRegulator:

    def __init__(self):
        self.rc = RelayController()
        self.sh = ScheduleHandler()
        self.ts = TemperatureSensor()
        self.regulator = Regulator()
        self.running = True

    def start(self, args):
        #1. Check if new schedule should be set
        if args.set_schedule != None:
            self.sh.setNewSchedule(args.set_schedule)

        #2. Print active schedule
        self.sh.printActiveSchedule()

        #3. Run application
        self.run()

    def run(self):
        while(self.running):
            #1. Check if we are done brewing
            if self.sh.brewingDone():
                self.running = False
            #2. Check if we should advance the schedule
            self.sh.advanceSchedule()
            targetTemp = self.sh.getTargetTemperature()
            #3. Perform pid
            self.regulator.pid(targetTemp)
            #4. Sleep
            time.sleep(10)

if __name__ == '__main__':

    br = BrewingRegulator()

    parser = argparse.ArgumentParser(description='Ninc Brewing Regulator version {}'.format(get_git_revision_short_hash()))

    sp_set_schedule = parser.add_argument('--set-schedule', help='Sets the active schedule')
    args = parser.parse_args()
    br.start(args)
