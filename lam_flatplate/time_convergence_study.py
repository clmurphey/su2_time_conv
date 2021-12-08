#!/usr/bin/env python

## \file time_convergence_study.py
#  \brief Python script for plotting time convergence from SU2 history.csv files.
#  \author Corey Murphey
#  \version 7.2.1 Blackbird
#
# The current SU2 release has been coordinated by the
# SU2 International Developers Society <www.su2devsociety.org>
# with selected contributions from the open-source community.
#
# The main research teams contributing to the current release are:
#  - Prof. Juan J. Alonso's group at Stanford University.
#  - Prof. Piero Colonna's group at Delft University of Technology.
#  - Prof. Nicolas R. Gauger's group at Kaiserslautern University of Technology.
#  - Prof. Alberto Guardone's group at Polytechnic University of Milan.
#  - Prof. Rafael Palacios' group at Imperial College London.
#  - Prof. Vincent Terrapon's group at the University of Liege.
#  - Prof. Edwin van der Weide's group at the University of Twente.
#  - Lab. of New Concepts in Aeronautics at Tech. Institute of Aeronautics.
#
# Copyright 2012-2019, Francisco D. Palacios, Thomas D. Economon,
#                      Tim Albring, and the SU2 contributors.
#
# SU2 is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# SU2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with SU2. If not, see <http://www.gnu.org/licenses/>.

from matplotlib import mlab
from matplotlib import pyplot as plt
import os
import time
import subprocess as sp
from numpy import *
import pandas as pd
from collections import OrderedDict
import matplotlib as mpl
mpl.use('Agg')

# dpi for figures
my_dpi = 100

# number or ranks to use
nRank = 2

# these are the commands for the SU2 and mesh generation runs
# user can switch between quad and tria meshes by changing the script
commands = ["mpirun -np %s SU2_CFD " % (nRank), "./create_grid_tria.py"]
# commands = ["SU2_CFD ./create_grid_quad.py"]

# SU2 config file name
fnames = ["lam_flatplate_unst_EI_1st.cfg",
          "lam_flatplate_unst_EI_2nd.cfg", "lam_flatplate_unst_EI_TS.cfg", "lam_flatplate.cfg"]

# list of variables from the current solver to plot
variables = ["rho", "rhou", "rhov", "rhoe"]

# set the legend tags for each config
legends = ["Dual-1st", "Dual-2nd", "Time Stepping", "SST"]

# set the filenames for our output files
filename = "SU2.out"

# number of mesh nodes for NxN tria and quad meshes
meshParam = [9,17,33,65,129,257]

# output format for images (png or eps)
imgfrm = 'png'

###############################################################################
# End user parameter selection. Begin execution below.
###############################################################################

# brief error checking
if len(commands) != 2 or len(fnames) != len(legends):
  print("Check lengths of input lists for commands, configs, and legends.")
  raise SystemExit

for iMesh in range(len(meshParam)-1):
  if (meshParam[iMesh+1]-1)/(meshParam[iMesh]-1) != 2:
    print("Script requires mesh size N to increase by a factor of 2. Please check list of sizes.")
    raise SystemExit

# some extra labels for plotting
symb = ['s', 'o', 'd', '^', '*']
colo = ['blue', 'green', 'orange', 'red', 'yellow']


# print initial statement about number of cases
print("Running " + str(len(fnames)) + " MMS cases.")

fig, ax = plt.subplots()
fig1, ax1 = plt.subplots()

result = []
# loop over all meshes in the grid study
i_s = 0
for j in range(len(fnames)):
  ax.cla() #clear axes
  # set the correct number for iConfig
  iConfig = j

  # build the SU2 command for this particular time step
  commandSU2 = commands[0]+fnames[iConfig]+" > "+filename

  # call SU2 to run the calculation
  sp.call(commandSU2, shell=True)

  # # parse the history file to extract the final computed error
  #plot just the case
  result.append(pd.read_csv("history.csv"))
  print("Case " + str(i_s+1) + " finished\n")
  # plot the results of all cases
  print("Plotting Case " + str(i_s+1)+"\n")

  #will plot all time steps if more than one. 
  ax.plot(result[j].iloc[:, [2]], result[j].iloc[:, [7]], marker=symb[j], 
            color=colo[j], linewidth=1.5, markersize=9, label=legends[j])
  ax.set_xlabel(result[j].columns.values[2])
  ax.set_ylabel(result[j].columns.values[7])
  ax.set_title(legends[j])
  ax.legend(loc="center left", bbox_to_anchor=(.9, 0.5), prop={'size': 6})
  fig.savefig(legends[j]+".png")

  # plot all results
  ax1.plot(result[j].iloc[:, [2]], result[j].iloc[:, [7]], marker=symb[j],
          color=colo[j], linewidth=1.5, markersize=9, label=legends[j])
  ax1.set_xlabel(result[j].columns.values[2])
  ax1.set_ylabel(result[j].columns.values[7])
  ax1.set_xlim(0,20)
  ax1.set_title(legends[j])
  ax1.legend(loc="center left", bbox_to_anchor=(.9, 0.5), prop={'size': 6})
  fig1.savefig("all_unst.png")
  i_s += 1


# plot the results of all cases
print("Run Complete") 

