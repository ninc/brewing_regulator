#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import os
import argparse
import git
import subprocess
from datetime import datetime

from RelayController import *
from TemperatureSensor import *

log = logging.getLogger(__name__)
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()


def main():
    
    #rc = RelayController()
    #rc.selfTest()
    #ts = TemperatureSensor()
    #ts.selfTest()

    print(datetime.now())


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ninc Brewing Regulator version {}'.format(get_git_revision_short_hash()))
    parser.add_argument('--start', help='Starts the application with the active schedule')
    parser.add_argument('--stop', help='Stops the application and turns off all relays')
    parser.add_argument('--set-schedule', help='Sets the active schedule')
    parser.add_argument('--print-schedule', help='Prints the active schedule')

    args = parser.parse_args()
    print(args)
    main()