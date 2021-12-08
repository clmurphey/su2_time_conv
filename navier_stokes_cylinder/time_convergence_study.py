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
commands = ["mpirun -np %s SU2_CFD " % (nRank), "./update_ts.py"]
# commands = ["SU2_CFD ./create_grid_quad.py"]

# SU2 config file name
fnames = ["lam_mms_jst_unst.cfg", "lam_mms_roe_wls_unst.cfg", "lam_mms_dg_unst.cfg"]

# list of variables from the current solver to plot
variables = ["rho", "rhou", "rhov", "rhoe"]

# set the legend tags for each config
legends = ["JST", "ROE+WLS", "DG"]

# set the filenames for our output files
filename = "SU2.out"

tm = [ "DUAL_TIME_STEPPING-1ST_ORDER",
      "DUAL_TIME_STEPPING-2ND_ORDER"] #can add "TIME_STEPPING"
tm_labels = ["Dual-1st", "Dual-2nd"] #Add label for "TIME_STEPPING" if you add that option above

td = ["EULER_IMPLICIT", "EULER_EXPLICIT", "RUNGE-KUTTA_EXPLICIT"]
td_labels = ["EI", "EE", "RKE"]

# output format for images (png or eps)
imgfrm = 'png'

###############################################################################
# End user parameter selection. Begin execution below.
###############################################################################

# brief error checking
if len(commands) != 2 or len(fnames) != len(legends):
  print("Check lengths of input lists for commands, configs, and legends.")
  raise SystemExit

# some extra labels for plotting
symb = ['s', 'o', 'd', '^', '*']
colo = ['blue', 'green', 'orange', 'red', 'yellow']


# print initial statement about number of cases
print("Running cases.")

fig, ax = plt.subplots()
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()

result = []
# loop over all meshes in the grid study
i_s = 0
for j in range(len(tm)):
  ax3.cla()
  for k in range(len(tm)):
    ax2.cla()
    for l in range(len(td)):
      ax.cla() #clear axes
      # set the correct number for iConfig
      iConfig = j

      # build the command to change the time step in the .cfg files
      commandGrid = commands[1] +  " -f %s -m %s -d %s" % (fnames[iConfig], tm[k], td[l])

      # update the config file with TIME_MARCHING scheme
      sp.call(commandGrid, shell=True)

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
      ax.plot(result[i_s].iloc[:, [2]], result[i_s].iloc[:, [6]], marker=symb[j], 
              color=colo[l], linewidth=1.5, markersize=9, label=legends[j]+": "+tm_labels[k] + "-" + td_labels[l])
      ax.set_xlabel(result[i_s].columns.values[2])
      ax.set_ylabel(result[i_s].columns.values[6])
      ax.set_title(legends[j]+": " + tm_labels[k] + "-" + td_labels[j])
      ax.legend(loc="upper right", prop={'size': 6})
      fig.savefig(legends[j]+tm_labels[k]+td_labels[l]+".png")
      
      #will plot all time steps if more than one.
      ax2.plot(result[i_s].iloc[:, [2]], result[i_s].iloc[:, [6]], marker=symb[j],
              color=colo[l], linewidth=1.5, markersize=9, label= td_labels[l])
      ax2.set_xlabel(result[i_s].columns.values[2])
      ax2.set_ylabel(result[i_s].columns.values[6])
      ax2.set_title(legends[j]+": " + tm_labels[k])
      ax2.legend(loc="upper right", prop={'size': 6})
      fig2.savefig(legends[j]+tm_labels[k]+".png")

      #will plot all time steps if more than one.
      ax3.plot(result[i_s].iloc[:, [2]], result[i_s].iloc[:, [6]], marker=symb[k],
               color=colo[l], linewidth=1.5, markersize=9, label=tm_labels[k] + "-" + td_labels[l])
      ax3.set_xlabel(result[i_s].columns.values[2])
      ax3.set_ylabel(result[i_s].columns.values[6])
      ax3.set_title(legends[j])
      ax3.legend(loc="upper right", prop={'size': 6})
      fig3.savefig(legends[j]+".png")

      # plot all results
      ax1.plot(result[i_s].iloc[:, [2]], result[i_s].iloc[:, [6]], marker=symb[k],
              color=colo[l], linewidth=1.5, markersize=9, label=legends[j]+": "+tm_labels[k] + "-" + td_labels[l])
      ax1.set_xlabel(result[i_s].columns.values[2])
      ax1.set_ylabel(result[i_s].columns.values[6])
      ax1.set_title("all")
      ax1.legend(loc="upper right", prop={'size': 6})
      fig1.savefig("all_unst.png")
      i_s += 1


# plot the results of all cases
print("Run Complete") 

