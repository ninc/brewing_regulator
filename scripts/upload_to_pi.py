#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

script_path = os.path.dirname(os.path.realpath(__file__))
script_path = script_path.replace('\\', '/')
file_path = script_path + '/../*'
test_path = script_path + '/../test/*'
service_path = script_path + '/../service/*'
pi_path = 'pi@46.59.41.137:/home/pi/project/brewing_regulator'

while True:
    cmd = 'scp -P 998 {} {}'.format(file_path, pi_path)
    print(cmd)
    os.system(cmd)

    cmd = 'scp -P 998 {} {}'.format(test_path, 'pi@46.59.41.137:/home/pi/project/brewing_regulator/test/')
    print(cmd)
    os.system(cmd)

    cmd = 'scp -P 998 {} {}'.format(service_path, 'pi@46.59.41.137:/home/pi/project/brewing_regulator/service/')
    print(cmd)
    os.system(cmd)

    time.sleep(1)