from lammps import lammps
from mpi4py import MPI
import time
import random
# from pylammpsmpi import LammpsLibrary
# from bayes_opt import BayesianOptimization
# from bayes_opt.util import UtilityFunction, Colours
import numpy as np
import asyncio
import threading
from ctypes import *

R_x = 0.8828
R_y = 0.8757
h =  15.2909
n = 6
cnum = 6
T = 0.832
M = 8e-07

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
# lmp.command("variable        hy equal %s" % hgtx)
# lmp.command("variable        hm equal %s" % hgty)

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

lmp.file("shearflow.lammps")




