#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 12:47:16 2021

@author: pedrorodriguez
"""

import simpy
import random
import matplotlib.pyplot as plt

print(f'STARTING SIMULATION')
print(f'------------------------------')


#-----------------------------------------------------
units_made = 0

#Units
units_capacity = 1200 #maximum amount of units that can be available at some point
initial_units = 0 #units available beginning of shift

#station_2
pre_station_2_capacity = 60 * 11 #60 units/hour 11 hours = 660 units
post_station_2_capacity = 60 * 11

#dispatch
dispatch_capacity = 1200 #maximum amount ot units at the end (output)

#-----------------------------------------------------

monthly_failed = 8
daily_failed = 8 / 24
shift_failed = daily_failed / 2
repair_time_1 = 750.34 / 60 #Divided by 60 to convert to min
break_mean_1 = 1 / repair_time_1

#-----------------------------------------------------

units = []
pre_station_2 = []

#-----------------------------------------------------

num_station_1 = 1
mean_station_1 = 17
std_station_1 = 2

num_station_2 = 1
mean_station_2 = 13
std_station_2 = 2

num_station_3 = 1
mean_station_3 = 15
std_station_3 = 2

#-----------------------------------------------------
critical_stock = 30
critical_station_2_stock = 20
#-----------------------------------------------------

class Production_line:
    def __init__(self, env):
        self.units = simpy.Container(env, capacity= units_capacity, init= initial_units)
        self.units_control = env.process(self.stock(env))
        self.pre_station_2 = simpy.Container(env, capacity= pre_station_2_capacity, init= 60)
        self.pre_station_2_control = env.process(self.station_2_stock(env))
        self.post_station_2 = simpy.Container(env, capacity= post_station_2_capacity, init= 60)
        self.dispatch = simpy.Container(env, capacity= dispatch_capacity, init= 60)
        self.broken = False

    def stock(self, env):
        yield env.timeout(0)
        while True:
            if self.units.level <= critical_stock:
                #print('Units bellow 30')
                #print('----------------------------------')
                yield env.timeout(1)
                yield self.units.put(30)
                #print('units stock is {0}'.format(self.units.level))
                #print('----------------------------------')
                yield env.timeout(8)
            else:
                yield env.timeout(1)

    def station_2_stock(self, env):
        yield env.timeout(0)
        while True:
            if self.pre_station_2.level <= critical_station_2_stock:
                yield env.timeout(1)
                yield self.pre_station_2.put(40)
                yield env.timeout(8)
            else:
                yield env.timeout(1)


def station_1_op(env, production_line):
        while True:
            yield production_line.units.get(13)
            #print('Station 1 received %d to process' % production_line.units.level)
            station_1_time = random.gauss(mean_station_1, std_station_1)
            yield env.timeout(station_1_time)
            yield production_line.pre_station_2.put(13)
            #print('Station 1 processed %d units' % production_line.pre_station_2.level)
            #print('----------------------------------')


units_produced_station_2 = []
obs_time_2 = []

def station_2_op(env, production_line):
        while True:
            yield production_line.pre_station_2.get(13)
            #print('Station 2 have %d to process' % production_line.pre_station_2.level)
            station_2_time = random.gauss(mean_station_2, std_station_2)
            yield env.timeout(station_2_time)
            yield production_line.post_station_2.put(13)
            #print('Station 2 precessed %d units' % production_line.post_station_2.level)
            #print('----------------------------------')
            units_produced_station_2.append(production_line.post_station_2.level)
            obs_time_2.append(env.now)

units_produced = []
obs_time = []

def station_3_op(env, production_line):
        while True:
            yield production_line.post_station_2.get(13)
            #print('Station 3 received %d to process' % production_line.post_station_2.level)
            station_3_time = random.gauss(mean_station_3, std_station_3)
            yield env.timeout(station_3_time)
            yield production_line.dispatch.put(12)
            #print('Station 3 precessed %d units' % production_line.dispatch.level)
            #print('----------------------------------')
            units_produced.append(production_line.dispatch.level)
            obs_time.append(env.now)


def observe(env, production_line):
    while True:
        obs_time.append(env.now)
        q_length.append(len(production_line.queue))
        yield env.timeout(0.5)

env = simpy.Environment()
production_line = Production_line(env)

station_1_op_process = env.process(station_1_op(env, production_line))
station_2_op_process = env.process(station_2_op(env, production_line))
station_3_op_process = env.process(station_3_op(env, production_line))


#-------------------------------------------------------------------------------

total_time_hr = 12
total_time_sec = total_time_hr * 60
shift_day = 1
total_time = total_time_sec * shift_day

#-------------------------------------------------------------------------------

env.run(until= total_time)


print(f'RUNNING TIME:', total_time_hr * shift_day, 'hours')
print(f'------------------------------')
#print(f'Station 1 has %d units to process' % production_line.pre_station_2.level)
#print(f'Station 2 has %d units to process' % production_line.post_station_2.level)
print(f'Production line has %d units processed' % production_line.dispatch.level)
#print(f'------------------------------')
#print(f'total units made: {0}'.format(units_made + production_line.dispatch.level))
print(f'------------------------------')
print(f'SIMULATION COMPLETED')

#plt.figure()
#plt.scatter(units_produced, obs_time)
#plt.show()

#plt.figure()
#plt.step(units_produced_station_2, obs_time_2, where= 'post')
#plt.show()
