#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 12:47:16 2021

@author: pedrorodriguez
"""

import simpy
import random

print(f'STARTING SIMULATION')
print(f'------------------------------')


#-----------------------------------------------------

#Units
units_capacity = 1200
initial_units = 600

#station_2
pre_station_2_capacity = 60
post_station_2_capacity = 60

#dispatch
dispatch_capacity = 1200


class Production_line:
    def __init__(self, env):
        self.units = simpy.Container(env, capacity= units_capacity, init= initial_units)
        self.pre_station_2 = simpy.Container(env, capacity= pre_station_2_capacity, init= 0)
        self.post_station_2 = simpy.Container(env, capacity= post_station_2_capacity, init= 0)
        self.dispatch = simpy.Container(env, capacity= dispatch_capacity, init= 0)

def station_1_op(env, production_line):
    while True:
        yield production_line.units.get(3)
        station_1_time = 1
        yield env.timeout(station_1_time)
        yield production_line.pre_station_2.put(3)

def station_2_op(env, production_line):
    while True:
        yield production_line.pre_station_2.get(3)
        station_2_time = 1
        yield env.timeout(station_2_time)
        yield production_line.post_station_2.put(3)

def station_3_op(env, production_line):
    while True:
        yield production_line.post_station_2.get(3)
        station_3_time = 1
        yield env.timeout(station_3_time)
        yield production_line.dispatch.put(3)


env = simpy.Environment()
production_line = Production_line(env)

station_1_op_process = env.process(station_1_op(env, production_line))
station_2_op_process = env.process(station_2_op(env, production_line))
station_3_op_process = env.process(station_3_op(env, production_line))

total_time_hr = 12
total_time_min = total_time_hr * 60
shift_day = 6
total_time = total_time_min * shift_day
env.run(until= total_time)

print(f'Dispatch has %d units produced' % production_line.dispatch.level)
print(f'------------------------------')
print(f'SIMULATION COMPLETED')
