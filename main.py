#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import os
import argparse
import subprocess
from datetime import datetime

from RelayController import *
from TemperatureSensor import *
from ScheduleHandler import *
from Regulator import *

log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=os.environ.get("LOGLEVEL", "INFO"))

def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

def startApplication(args):
    """Starts the applications, sets up timers to wake up to regulate and advance schedule"""
    log.info('Starting application')
    #TODO: Set up crontab jobs

def stopApplication(args):
    """Stops the application dead"""
    log.info('Stopping application')
    #TODO: Remove crontab jobs
    rc = RelayController()
    rc.setAllRelaysOff()

def setSchedule(args):
    """Sets the active schedule"""
    log.info('Setting new schedule')
    sc = ScheduleHandler()
    sc.setNewSchedule(args.schedule)

def printSchedule(args):
    """Prints the current schedule"""
    log.info('Active schedule:')
    sc = ScheduleHandler()
    sc.printActiveSchedule()

def regulate(args):
    """Checks the temperature and takes appropriate action"""
    log.info('Regulate')
    sc = ScheduleHandler()
    #TODO Check time
    targetTemp = sc.getTargetTemperature()

    if targetTemp == None:
        log.info('Brewing not started')
        return

    regulator = Regulator(targetTemp)
    regulator.pid()


def advanceSchedule(args):
    """Advances the schedule to the next schedule item"""
    sc = ScheduleHandler()
    sc.advanceSchedule()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ninc Brewing Regulator version {}'.format(get_git_revision_short_hash()))
    sub_parser = parser.add_subparsers()
    sp_start = sub_parser.add_parser('start', help='Starts the application with the active schedule')
    sp_start.set_defaults(func=startApplication)
    sp_stop = sub_parser.add_parser('stop', help='Stops the application and turns off all relays')
    sp_stop.set_defaults(func=stopApplication)
    sp_set_schedule = sub_parser.add_parser('set-schedule', help='Sets the active schedule')
    sp_set_schedule.add_argument('schedule', help='The schedule file')
    sp_set_schedule.set_defaults(func=setSchedule)
    sp_print_schedule = sub_parser.add_parser('print-schedule', help='Prints the active schedule')
    sp_print_schedule.set_defaults(func=printSchedule)
    sp_regulate = sub_parser.add_parser('regulate',
        help='The regulator takes actions to regulate the temperature according to the current schedule. This is usally done by the crontab job')
    sp_regulate.set_defaults(func=regulate)
    sp_set_new_timer = sub_parser.add_parser('advance-schedule',
        help='The regulator will advance the schedule. This is usally done by the crontab job')
    sp_set_new_timer.set_defaults(func=advanceSchedule)

    args = parser.parse_args()
    args.func(args)
