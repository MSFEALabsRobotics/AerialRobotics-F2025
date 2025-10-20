# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2014 Bitcraze AB
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
Simple example that connects to the first Crazyflie found, ramps up/down
the motors and disconnects.
"""
import logging
import time
from threading import Thread
from threading import Timer
import _thread
import sys
sys.path.append('/home/bitcraze/Desktop/projects/crazyflie-lib-python/cflib/positioning/')
sys.path.append('/home/bitcraze//Desktop/projects/crazyflie-lib-python/')


import cflib

from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig

logging.basicConfig(level=logging.ERROR)


class FlyPath:
    """Example that connects to a Crazyflie and ramps the motors up/down and
    the disconnects"""

    

    def __init__(self, link_uri):
        """ Initialize and run the example with the specified link_uri """

        self._cf = Crazyflie()

        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)

        print('Connecting to %s' % link_uri)

        self._cf.open_link(link_uri)

        # Variable used to keep main loop occupied until disconnect
        self.is_connected = True

        self._alt=9999
        self._newdata=False
        self._timer_on=False

        self.roll=0
        self.pitch=0
        self.yawrate=0

        self._accx=0
        self._accy=0
        self._accz=0

        #TimeOut is the time afterwhich the aircraft disconnects
        self._TimeOut=30

        self._Go=True

    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""
        print('Connected to %s' % link_uri)
    
        # The definition of the logconfig can be made before connecting
        self._lg_alt = LogConfig(name='Kalman Variance', period_in_ms=500)

        #Set the logconfig to read specific values
        self._lg_alt.add_variable('kalman.varPX', 'float')
        self._lg_alt.add_variable('kalman.varPY', 'float')
        self._lg_alt.add_variable('kalman.varPZ', 'float')

        # Adding the configuration cannot be done until a Crazyflie is
        # connected, since we need to check that the variables we
        # would like to log are in the TOC.
        try:
            self._cf.log.add_config(self._lg_alt)
            # This callback will receive the data
            self._lg_alt.data_received_cb.add_callback(self._alt_log_data)
            # This callback will be called on errors
            self._lg_alt.error_cb.add_callback(self._alt_log_error)
            # Start the logging
            self._lg_alt.start()
            print('Logging Started')
        except KeyError as e:
            print('Could not start log configuration,'
                  '{} not found in TOC'.format(str(e)))
        except AttributeError:
            print('Could not add Stabilizer log config, bad configuration.')

        # Start a timer to disconnect in 10s
        t = Timer(self._TimeOut, self._cf.close_link)
        t.start()

    def _alt_log_error(self, logconf, msg):
        """Callback from the log API when an error occurs"""
        print('Error when logging %s: %s' % (logconf.name, msg))

    def _alt_log_data(self, timestamp, data, logconf):
        """Callback froma the log API when data arrives"""
            #print('[%d][%s]: %s' % (timestamp, logconf.name, data))
        #Every time data is received newdata flag is set
        self._newdata=True
        #Update the values of the variables received
        self._alt=float(data["kalman.varPZ"])
        self._accx=float(data["kalman.varPX"])
        self._accy=float(data["kalman.varPY"])
        self._accz=float(data["kalman.varPZ"])

        #GET THE ALT DATA FROM HERE
        #GET THE ACCELERATION FROM HERE

    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the specified address)"""
        print('Connection to %s failed: %s' % (link_uri, msg))
        self.is_connected = False

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print('Connection to %s lost: %s' % (link_uri, msg))

    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print('Disconnected from %s' % link_uri)
        self.is_connected = False

    
    def _timer_turned_off(self):
        #This function is called by the Timer thread in order to flag the expiry of the set timer
        self._timer_on=False


    def _Move_Dir(self,Action,Dir_Time,Dir_Angle,thrust):
        #This function allows the setting of a single action from specified in 
        #the variable Action (P or p for Pitch, R or r for Roll and Y or y for Yawrate)
        #The action is set for a defined duration in seconds Dir_Time
        #The action sets a certain angle in degrees specified in Dir_Angle, 
        # note Dir_Angle for Yawrate is the rate of yaw specified in degrees/seconds
     
        #Start the timer
        self._timer_on=True
        tm = Timer(Dir_Time, self._timer_turned_off)
        tm.start()

        #Remove any previous angle settings
        self.roll=0
        self.pitch=0
        self.yawrate=0

        #Set the appropriate angle
        if Action =="P" or Action =="p":
            self.pitch=Dir_Angle
        elif Action =="R" or Action =="r":
            self.roll=Dir_Angle
        elif Action =="Y" or Action =="y":
            self.yawrate=Dir_Angle
        print ('Moving_'+str(Action)+ str(Dir_Angle))

        #Keep sending the command every 200 ms, if no command is received within 500 ms the aircraft will shut off
        #Check that the timer hasn't expired, the aircraft is connected and the emergency stop button is not pressed 
        while self._timer_on and self.is_connected and self._Go:
            self._cf.commander.send_setpoint(self.roll, self.pitch, self.yawrate, thrust)
            time.sleep(0.2)

        #Once the action is completed reset the aircrafts' attitude to zero
        self._cf.commander.send_setpoint(0,0,0, thrust)
        print ('Move complete')

    def _Ascend(self,Climb_Time,Asc_thrust,Hold_thrust):
        #This function will climb the aircraft based on the ascending thrust Ascthrust
        #for a defined time in seconds specified by Climb_Time
        #and then switch into maintaining an altitude using Mainthrust
        #Start the timer
        self._timer_on=True
        tm = Timer(Climb_Time, self._timer_turned_off)
        tm.start()
        print ('Taking-Off...')

        #Keep sending the command every 200 ms, if no command is received within 500 ms the aircraft will shut off
        #Check that the timer hasn't expired, the aircraft is connected and the emergency stop button is not pressed 
        while self._timer_on and self.is_connected and self._Go:
            self._cf.commander.send_setpoint(0,0,0, Asc_thrust)
            time.sleep(0.2)

        #Once the climb is completed switch the thrust value into Mainthrust
        self._cf.commander.send_setpoint(0,0,0, Hold_thrust)
        print ('Take-Off complete')
    
    def _Land(self,Dec_Time,Dec_thrust):
        #This function will descend the aircraft based on the descending thrust Dec_thrust
        #for a defined time in seconds specified by Dec_Time
        #and then switch off the motors
        #Start the timer
        self._timer_on=True
        tm = Timer(Dec_Time, self._timer_turned_off)
        tm.start()
        print ('Landing...')

        #Keep sending the command every 200 ms, if no command is received within 500 ms the aircraft will shut off
        #Check that the timer hasn't expired, the aircraft is connected and the emergency stop button is not pressed 
        while self._timer_on and self.is_connected and self._Go:
            self._cf.commander.send_setpoint(0,0,0, Dec_thrust)
            time.sleep(0.2)

        #Once the landing is completed shutdwon the motors
        self._cf.commander.send_setpoint(0,0,0,0)
        print ('Landing complete')


    def _Hold(self,thrust,Time):
        #This function is used to hold an attitude at a certain thrust level for a period of time 
        self._timer_on=True
        tm = Timer(Time, self._timer_turned_off)
        tm.start()
        print ('Holding...')
        while self._timer_on and self.is_connected and self._Go:
            self._cf.commander.send_setpoint(0,0,0, thrust)
            time.sleep(0.2)
        print ('Holding complete')


    def _Do_Mission (self):
          
        #INITIALISATION
        while not self._newdata:
            time.sleep(0.1)
        # Unlock startup thrust protection
            self._cf.commander.send_setpoint(0, 0, 0, 0)


    ####################################################################    
    #                      DEFINE VARIABLES                            #
        Time = 2
        Yaw_Rate = 90
        Asc_thrust = 45000
        Hold_thrust = 38000
        Dec_thrust = 35000
        Climb_Time = 1.5
    #                                                                  #
    ####################################################################
        
    ####################################################################    
    #                          FLIGHT PLAN                             # 
    #         Place your flight plan code in the space below           #
    ####################################################################
    #                                                                  #   
        #Commencing Take-Off...
        self._Ascend(Climb_Time,Asc_thrust,Hold_thrust)

        #Holding...
        self._Hold(Hold_thrust,1)

        #Going Forwards...'
        self._Move_Dir('P',0.4,10,Hold_thrust)

        #Holding...
        self._Hold(Hold_thrust,1)

        #Going Backwards...'
        self._Move_Dir('P',0.4,-8,Hold_thrust)

        #Holding...
        self._Hold(Hold_thrust,1)

        #Landing
        self._Land(2.5,Dec_thrust)
    #                                                                   # 
    ####################################################################    
    
    def _DisplayInfo(self):
        c= input("Use E for Emergency Stop")
        if c=="E" or c=="e":
            print ("Emergency STOP!")
            self._cf.commander.send_setpoint(0,0,0,0)
            self._Go=False
            self._cf.close_link()

if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    # Scan for Crazyflies and use the first one found
    print('Scanning interfaces for Crazyflies...')
    available = cflib.crtp.scan_interfaces()
    print('Crazyflies found:')
    for i in available:
        print(i[0])

    if len(available) > 0:

    ####################################################################    
    #                         RADIO SETTINGS                           #                          
    #        Use the following: "radio://0/Your_Channel/1M"            #
    #  NOTE: Bandwidth should be set to 1M not 250K shown in lab sheet #
    ####################################################################
    #                                                                  #
        le = FlyPath("radio://0/70/2M")
    #                                                                  #     
    ####################################################################

        _thread.start_new_thread(le._DisplayInfo,())
        _thread.start_new_thread(le._Do_Mission,()) #For 90

        while le.is_connected:
            time.sleep(1)

    else:
        print('No Crazyflies found, cannot run example')
