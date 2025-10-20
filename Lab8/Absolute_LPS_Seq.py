# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2016 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
Simple example that connects to one crazyflie (check the address at the top
and update it to your crazyflie address) and send a sequence of setpoints,
one every 5 seconds.

This example is intended to work with the Loco Positioning System in TWR TOA
mode. It aims at documenting how to set the Crazyflie in position control mode
and how to send setpoints.
"""
import time
import sys

sys.path.append('/home/bitcraze/Desktop/projects/crazyflie-lib-python/')

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger

#########################################################################
# URI to the Crazyflie to connect to.
# Change 10 below to your Crazflie's radio channel.
#########################################################################
uri = 'radio://0/70/2M'

#########################################################################
# Add your sequence/s below.
# Each line in the array represents a Crazyflie setpoint (pose).
# defined as: (x, y, z, yaw)
# 5 seconds will be allocated for the Crazyflie to reach each position.
#########################################################################

offset_x = 0.0
# offset_x = 3.6

# Go to target land and come back
sequence0_a1 = [
(offset_x + 1.5, -1.0, 1.0, 0),
(offset_x + 1.5, 0.0, 1.0, 90),
(offset_x + 1.5, 1.0, 1.0, 90),
]

sequence1_a1 = [
(offset_x + 1.0, 1.05, 1.0, -90),
(offset_x + 1.0, 1.05, 1.0, -90),
(offset_x + 1.0, -0.7, 1.0, -90),
]



def wait_for_position_estimator(scf):
    print('Waiting for estimator to find position...')

    log_config = LogConfig(name='Kalman Variance', period_in_ms=500)
    log_config.add_variable('kalman.varPX', 'float')
    log_config.add_variable('kalman.varPY', 'float')
    log_config.add_variable('kalman.varPZ', 'float')

    var_y_history = [1000] * 10
    var_x_history = [1000] * 10
    var_z_history = [1000] * 10

    threshold = 0.001

    with SyncLogger(scf, log_config) as logger:
        for log_entry in logger:
            data = log_entry[1]

            var_x_history.append(data['kalman.varPX'])
            var_x_history.pop(0)
            var_y_history.append(data['kalman.varPY'])
            var_y_history.pop(0)
            var_z_history.append(data['kalman.varPZ'])
            var_z_history.pop(0)

            min_x = min(var_x_history)
            max_x = max(var_x_history)
            min_y = min(var_y_history)
            max_y = max(var_y_history)
            min_z = min(var_z_history)
            max_z = max(var_z_history)

            # print("{} {} {}".
            #       format(max_x - min_x, max_y - min_y, max_z - min_z))

            if (max_x - min_x) < threshold and (
                    max_y - min_y) < threshold and (
                    max_z - min_z) < threshold:
                break


def reset_estimator(scf):
    cf = scf.cf
    cf.param.set_value('kalman.resetEstimation', '1')
    time.sleep(0.1)
    cf.param.set_value('kalman.resetEstimation', '0')

    wait_for_position_estimator(cf)


def position_callback(timestamp, data, logconf):
    x = data['kalman.stateX']
    y = data['kalman.stateY']
    z = data['kalman.stateZ']
    print('pos: ({}, {}, {})'.format(x, y, z))


def start_position_printing(scf):
    log_conf = LogConfig(name='Position', period_in_ms=500)
    log_conf.add_variable('kalman.stateX', 'float')
    log_conf.add_variable('kalman.stateY', 'float')
    log_conf.add_variable('kalman.stateZ', 'float')

    scf.cf.log.add_config(log_conf)
    log_conf.data_received_cb.add_callback(position_callback)
    log_conf.start()


def run_sequence(cf, sequence):
    for position in sequence:
        print('Setting position {}'.format(position))
        for i in range(50):
            cf.commander.send_position_setpoint(position[0],
                                                position[1],
                                                position[2],
                                                position[3])
            # Must send once every 100ms for crazyflie to think it is still connected.
            time.sleep(0.1)


# Lands the crazyflie in a number of fixed sized steps.
# The number of steps is determined by the by height/step size.
def land(cf, position):
    print("Landing...")
    step_height_m = 0.05
    start_height_m = position[2]
    num_steps = int((start_height_m / step_height_m)) + 1
    new_height_m = start_height_m - step_height_m 
    # Must send once every 200ms for crazyflie to think it is still connected.
    for i in range(0, num_steps):
        print("Landing height", new_height_m)
        cf.commander.send_position_setpoint(position[0],
                                            position[1],
                                            new_height_m,
                                            position[3])
        new_height_m -= step_height_m
        time.sleep(0.2)
    print("Landed")


def stop(cf):
    cf.commander.send_stop_setpoint()
    # Make sure that the last packet leaves before the link is closed
    # since the message queue is not flushed before closing
    time.sleep(1.0)


#########################################################################
# run_sequence_and_land takes the following arguments:
# scf       synchronised crazyflie object (the connected Crazyflie).
# sequence  an array of crazyflie setpoint positions.
#
# Crazyflie executes each position in the sequence in turn then lands.
#########################################################################
def run_sequence_and_land(scf, sequence):
    cf = scf.cf
    run_sequence(cf, sequence)
    land(cf, sequence[-1])
    stop(cf)


#########################################################################
# Main Program Entry Point
#########################################################################
if __name__ == '__main__':
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        reset_estimator(scf)
        start_position_printing(scf)
#########################################################################
# Modify the code for each arena between here...
        run_sequence_and_land(scf, sequence0_a1)
        run_sequence_and_land(scf, sequence1_a1)
# and here
#########################################################################
    print("Finished!")
    scf.cf.close_link()


