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

def biofilm_shear(R_x, R_y, h, n):
    R_x = np.array(R_x)
    R_y = np.array(R_y)
    h = np.array(h)
    n = np.array(n)
    n = int(n)
    unit_cell_length = 4e-5 / n
    unit_lattice = unit_cell_length / 4e-7
    R_x = R_x * unit_lattice
    R_x = R_x / 2
    R_y = R_y * unit_lattice
    R_y = R_y / 2
    R_x = np.around(R_x, decimals = 1) # Only save 1 decimal to prevent geo. errors
    R_y = np.around(R_y, decimals = 1)
    h = np.around(h, decimals = 1)
    varx = float(R_x)#str(3)
    vary = float(R_y)
    hgtx = float(h)
    hyplus = hgtx + 2
    hyplus = float(hyplus)
    hgty = hyplus + 3
    hgty = float(hgty)
    cnum = int(n) #number of cones of substrate

    if varx < vary:
        varx = float(R_y)
        vary = float(R_x)

    if varx < 1:
        varx = 1
    if vary < 1:
        vary = 1
        
    print(varx)
    print(vary)
    print(hgtx)
    print(hyplus)
    print(hgty)
    print(n)
    lmp = lammps() # Open LAMMPS and recall the simulation
    lmp.command("variable        rx equal %s" % varx) # Read vars
    lmp.command("variable        ry equal %s" % vary)
    lmp.command("variable        hy equal %s" % hgtx)
    lmp.command("variable        hm equal %s" % hgty)

    if cnum == 10:
        lmp.file("geo_10.lammps")
    if cnum == 9:
        lmp.file("geo_9.lammps")
    if cnum == 8:
        lmp.file("geo_8.lammps")
    if cnum == 7:
        lmp.file("geo_7.lammps")
    if cnum == 6:
        lmp.file("geo_6.lammps")
    if cnum == 5:
        lmp.file("geo_5.lammps")

    substrate = lmp.get_natoms() # Read No. of atoms in susbtrate
    substrate = np.array(substrate)
    lmp.close() # Close LAMMPS after computing the total number of substrate

    lmp = lammps() # Open LAMMPS to conduct the "shear flow" simulation
    lmp.command("variable        rx equal %s" % varx) # Read vars
    lmp.command("variable        ry equal %s" % vary)
    lmp.command("variable        hy equal %s" % hgtx)
    lmp.command("variable        hm equal %s" % hgty)
    lmp.command("variable        hyplus equal %s" % hyplus)

    if cnum == 10:
        lmp.file("comp_10.lammps")
    if cnum == 9:
        lmp.file("comp_9.lammps")
    if cnum == 8:
        lmp.file("comp_8.lammps")
    if cnum == 7:
        lmp.file("comp_7.lammps")
    if cnum == 6:
        lmp.file("comp_6.lammps")
    if cnum == 5:
        lmp.file("comp_5.lammps")
    lmp.file("shearflow.lammps")
    total = lmp.get_natoms() # Read total No. of atoms 
    lmp.close()
    total = np.array(total) # Get the total number of "substrate + biofilm" -> NumPy array
    print(total)

    bacnum = total - substrate# # Compute No. of bacteria cells
    print(bacnum)

    biofilm_num = - bacnum # Maximize the negative value (minimize the toal bacteria numbers)
    return biofilm_num


from bayes_opt import BayesianOptimization

# Bounded region of parameter space
pbounds = {'R_x': (0.1, 0.9), 'R_y': (0.1, 0.9), 'h': (15, 20), 'n': (5.0, 10.9)} # Set bounds

utility = UtilityFunction(kind="ucb", kappa=2.5, xi=1) # GP Upper Confidence Bound

# ======SHEAR OPTIMIZATION======

opt_shear = BayesianOptimization(
    f=biofilm_shear,
    pbounds=pbounds,
    verbose=2,
    random_state=1,
)

# Probe the next point in shear simulation
next_point_shear = opt_shear.suggest(utility)
target_shear = biofilm_shear(**next_point_shear)
opt_shear.register(
    params=next_point_shear,
    target=target_shear,
)

# Create iterations for biofilm shear simulation
# for _ in range(100):
#     next_point = opt_shear.suggest(utility)
#     target = biofilm_shear(**next_point)
#     opt_shear.register(params=next_point, target=target)
    
#     print(target, next_point)
# print(opt_shear.max)

opt_shear.maximize(
    init_points=10,
    n_iter=90,
    alpha=1e-3,
)

for i, res in enumerate(opt_shear.res):
    print("Iteration {}: \n\t{}".format(i, res))
    

from bayes_opt.logger import JSONLogger
from bayes_opt.event import Events
logger_shear = JSONLogger(path="./shear_logs.json") # Save the model
opt_shear.subscribe(Events.OPTIMIZATION_STEP, logger_shear)

