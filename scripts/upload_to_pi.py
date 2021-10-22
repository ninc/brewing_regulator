#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

script_path = os.path.dirname(os.path.realpath(__file__))
script_path = script_path.replace('\\', '/')
file_path = script_path + '/../*'
pi_path = 'pi@192.168.1.212:/home/pi/project/brewing_regulator'


while True:
    cmd = 'scp -r {} {}'.format(file_path, pi_path)
    print(cmd)
    os.system(cmd)
    time.sleep(1)