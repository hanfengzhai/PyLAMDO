from lammps import lammps
from mpi4py import MPI
import time
import random
# from pylammpsmpi import LammpsLibrary
from bayes_opt import BayesianOptimization
from bayes_opt.util import UtilityFunction, Colours
import numpy as np
import asyncio
import threading
from ctypes import *

def biofilm_vib(R_x, R_y, h, n, T, M):
    R_x = np.array(R_x) # bottom radius
    R_y = np.array(R_y) # upper radius
    h = np.array(h) # hight
    n = np.array(n) # no. of cones
    n = int(n) # taken as integer
    unit_cell_length = 4e-5 / n # compute length of unit cell in SI unit (box)
    unit_lattice = unit_cell_length / 4e-7 # compute unit cell length in lattice unit
    R_x = R_x * unit_lattice # compute randomized unit cell length in lattice unit (bottom)
    R_y = R_y * unit_lattice # upper
    R_x = R_x / 2
    R_y = R_y / 2
    R_x = np.around(R_x, decimals = 1) # bottome radius -> Only save 1 decimal to prevent geo. errors
    R_y = np.around(R_y, decimals = 1) # upper radius -> Only save 1 decimal to prevent geo. errors
    h = np.around(h, decimals = 1) # height -> Only save 1 decimal to prevent geo. errors

    T = np.array(T) #frequency -> numpy array
    M = np.array(M) #vibration magnitude -> numpy array

    varx = float(R_x) # randomized bottom radius -> taken as float
    vary = float(R_y) # randomized upper radius -> taken as float
    h = float(h) # randomized height -> taken as float
    bot_coor = M/4e-7 #Distance in SI unit -> No. of particles
    bot_coor = float(bot_coor) 
    top_coor = bot_coor + 10 
    hx = top_coor#+1
    hy = hx + h
    hm = hy + 5
    # hgty = float(hgty)
    Tpe = float(T)
    Mag = float(M)
    cnum = int(n) #number of cones of substrate
    hy_vib = 11 + h
    hy_vib = float(hy_vib)
    hm_vib = hy_vib + 9
    hm_vib = float(hm_vib)
    hy_vib = np.around(hy_vib, decimals = 1)
    hm_vib = np.around(hm_vib, decimals = 1)
    hx = np.around(hx, decimals = 1)
    hy = np.around(hy, decimals = 1)
    hyplus = hy + 5
    hm = np.around(hm, decimals = 1)
    bot_coor = np.around(bot_coor, decimals = 1)
    top_coor = np.around(top_coor, decimals = 1)

    if varx < vary:
        varx = float(R_y)
        vary = float(R_x)
        
    print(varx)
    print(vary)
    print(bot_coor)
    print(top_coor)
    print(hx)
    print(hy)
    print(hyplus)
    print(hm)
    # print(h)
    print(n)
    if varx < 1:
        varx = 1
    if vary < 1:
        vary = 1

    lmp = lammps() # Open LAMMPS and recall the simulation
    lmp.command("variable        rx equal %d" % varx) # Read vars.
    lmp.command('variable        ry equal %d' % vary)
    lmp.command('variable        hy equal %d' % hy)
    lmp.command('variable        hy_plus equal %d' % hyplus)
    lmp.command('variable        hm equal %d' % hm)
    lmp.command('variable        hx equal %d' % hx)
    lmp.command('variable        subcor equal %d' % bot_coor)
    lmp.command('variable        topcor equal %d' % top_coor)

    if cnum == 10:
        lmp.file("geo_vib_10.lammps")
    if cnum == 9:
        lmp.file("geo_vib_9.lammps")
    if cnum == 8:
        lmp.file("geo_vib_8.lammps")
    if cnum == 7:
        lmp.file("geo_vib_7.lammps")
    if cnum == 6:
        lmp.file("geo_vib_6.lammps")
    if cnum == 5:
        lmp.file("geo_vib_5.lammps")

    substrate = lmp.get_natoms() # Read No. of atoms in susbtrate
    substrate = np.array(substrate)
    lmp.close() # Close LAMMPS after computing the total number of substrate

    lmp = lammps() # Open LAMMPS to conduct the "shear flow" simulation
    lmp.command("variable        rx equal %d" % varx) # Read vars.
    lmp.command('variable        ry equal %d' % vary)
    lmp.command('variable        hy equal %d' % hy)
    lmp.command('variable        hy_plus equal %d' % hyplus)
    lmp.command('variable        hm equal %d' % hm)
    lmp.command('variable        hx equal %d' % hx)
    lmp.command('variable        subcor equal %d' % bot_coor)
    lmp.command('variable        topcor equal %d' % top_coor)

    if cnum == 10:
        lmp.file("vibration_10_perio.lammps")
    if cnum == 9:
        lmp.file("vibration_9_perio.lammps")
    if cnum == 8:
        lmp.file("vibration_8_perio.lammps")
    if cnum == 7:
        lmp.file("vibration_7_perio.lammps")
    if cnum == 6:
        lmp.file("vibration_6_perio.lammps")
    if cnum == 5:
        lmp.file("vibration_5_perio.lammps")

    freq = float(T)
    M_half = M/2
    Mag = float(M_half)
    freq = np.around(freq, decimals = 6)
    Mag = np.around(Mag, decimals = 8)
    print(freq)
    print(Mag)
    lmp.command("variable Tpe equal %s" % freq)
    lmp.command("variable Mag equal %s" % Mag)
    lmp.file("vibration_lat.lammps")

    total = lmp.get_natoms() # Read total No. of atoms 
    lmp.close()
    total = np.array(total) # Get the total number of "substrate + biofilm" -> NumPy array
    print(total)

    bacnum = total - substrate# # Compute No. of bacteria cells
    print(bacnum)

    bacteria_num = - bacnum # Maximize the negative value (minimize the toal bacteria numbers)
    return bacteria_num


from bayes_opt import BayesianOptimization

# Bounded region of parameter space
pbounds = {'R_x': (0.1, 0.9), 'R_y': (0.1, 0.9), 'h': (5, 10), \
        'n': (5.0, 10.9), 'T': (1e-5, 1), 'M':(8e-7, 4e-6)} # Set bounds

utility = UtilityFunction(kind="ucb", kappa=2.5, xi=1) # GP Upper Confidence Bound

# ======VIBRATION OPTIMIZATION======

opt_vib = BayesianOptimization(
    f=biofilm_vib,
    pbounds=pbounds,
    verbose=2,
    random_state=1,
)

# Probe the next point in vibration simulation
next_point_vib = opt_vib.suggest(utility)
target_vib = biofilm_vib(**next_point_vib)
opt_vib.register(
    params=next_point_vib,
    target=target_vib,
)


opt_vib.maximize(
    init_points=10,
    n_iter=90,
    alpha=1e-3,
)

for i, res in enumerate(opt_vib.res):
    print("Iteration {}: \n\t{}".format(i, res))

from bayes_opt.logger import JSONLogger
from bayes_opt.event import Events
logger_vib = JSONLogger(path="./vib_logs.json") # Save the model
opt_vib.subscribe(Events.OPTIMIZATION_STEP, logger_vib)
