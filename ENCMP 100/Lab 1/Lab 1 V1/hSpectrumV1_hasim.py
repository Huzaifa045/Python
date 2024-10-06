## HSPECTRUM  Quantum Chemistry and the Hydrogen Emission Spectrum
#
# The periodic table is central to chemistry. According to Britannica,
# "Detailed understanding of the periodic system has developed along with
# the quantum theory of spectra and the electronic structure of atoms,
# beginning with the work of Bohr in 1913." In this lab assignment, a
# University of Alberta student explores the Bohr model's accuracy in
# predicting the hydrogen emission spectrum, using observed wavelengths
# from a US National Institute of Standards and Technology database.
#
# Copyright (c) 2022, University of Alberta
# Electrical and Computer Engineering
# All rights reserved.
#
# Student name: 
# Student CCID: 
# Others:
#
# To avoid plagiarism, list the names of persons, Version 0 author(s)
# excluded, whose code, words, ideas, or data you used. To avoid
# cheating, list the names of persons, excluding the ENCMP 100 lab
# instructor and TAs, who gave you compositional assistance.
#
# After each name, including your own name, enter in parentheses an
# estimate of the person's contributions in percent. Without these
# numbers, adding to 100%, follow-up questions will be asked.
#
# For anonymous sources, enter pseudonyms in uppercase, e.g., SAURON,
# followed by percentages as above. Email a link to or a copy of the
# source to the lab instructor before the assignment is due.
#
import numpy as np
import matplotlib.pyplot as plt

## EXPERIMENT DATA
#
data = [656.460,486.271,434.1692,410.2892, 397.1198, 389.0166, 383.6485] # nm
nist = np.array(data)
n = len(nist)

## MODEL SETUP
#
eMass = 9.1093836e-31 # electron mass
fundCharge = 1.6021766e-19 # fundamental charge
permFreeSpace = 8.8541878e-12 # permittivity of free spacce
planckConst = 6.6260702e-34 # plancks constant
speedOfLight = 2.9979246e8 # speed of light
rydberg = 1.0973732e7 # 1/m

# Expression for the predicted value of R according to Bohr's Model
rydberg = eMass * fundCharge**4 / (8 * permFreeSpace**2 * planckConst**3 * speedOfLight)  # 1/m

print("Rydberg constant:",int(round(rydberg)), "1/m")

## SIMULATION DATA
#
nf = input("Final state (nf): ")
nf = int(nf)
ni = np.arange(nf+1,nf+n+1)
plt.plot(ni,nist,'bx', label='NIST Data') # label added for legend

# Calculate wavelengths using the Bohr model
bohrWave = 1 / (rydberg * ((1 / nf**2) - (1 / ni**2)))

# Plot Bohr model points with unit conversion from m to nm
# round red dots for plot
# label added for legend
plt.plot(ni, bohrWave * 1e9, 'ro', label='Bohr Model', markersize = 4) 
 
# x and y axes labels
plt.xlabel('Initial State (ni)')
plt.ylabel('Wavelength (nm)')

# add legend for plot
plt.legend()

#add title for graph
plt.title("The Hydrogen Emission Spectrum - Observed and The Bohr Model")

plt.grid(True)
plt.show()
