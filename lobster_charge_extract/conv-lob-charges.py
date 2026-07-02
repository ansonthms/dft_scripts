#!/usr/bin/env python3
##Script to quickly convert LOBSTER-computed charges to an extxyz structure with charges read from CHARGE.lobster file
##Usage: python conv-lob-charges.py
import sys,os
import numpy as np
from ase.io import read, write
from pymatgen.io.lobster.outputs import Charge

if not os.path.isfile("CHARGE.lobster") and os.path.isfile("POSCAR.lobster.vasp"):
    exit()
# ASE reads QE input files directly
atoms = read('POSCAR.lobster.vasp')

# read ACF.dat — skip 2 header lines, drop last 4 summary lines
charge = Charge(filename='CHARGE.lobster')
mulliken=charge.mulliken
loewdin=charge.loewdin

atoms.set_initial_charges(mulliken)
filename='mulliken'+'.xyz'
print(filename)
atoms.write(filename)
print(f"Written: {filename}.xyz")

atoms.set_initial_charges(loewdin)
filename='loewdin'+'.xyz'
print(filename)
atoms.write(filename)
print(f"Written: {filename}.xyz")
