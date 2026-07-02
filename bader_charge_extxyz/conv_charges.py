#!/usr/bin/env python3
###Script to extract bader charges to an ase file with charges for easy visualization

import sys,os
import numpy as np
from ase.io import read, write

if len(sys.argv) != 2:
    print("Usage: conv_charge.py <path to structure>. Make sure to run in folder containing ACF.dat")
    exit()
basename=os.path.basename(sys.argv[1])


val_electrons = {"Al": 3, "O": 6, "H": 1, "Cl": 7}

# ASE reads QE input files directly
atoms = read(sys.argv[1], format='espresso-in')

# read ACF.dat — skip 2 header lines, drop last 4 summary lines
data = np.loadtxt("ACF.dat", skiprows=2, max_rows=len(atoms))
bader_charges = data[:, 4]  # column 5 (0-indexed: 4)

# net charge = valence electrons - bader charge
symbols = atoms.get_chemical_symbols()
net_charges = np.array([val_electrons[s] - q for s, q in zip(symbols, bader_charges)])

atoms.set_initial_charges(net_charges)

jobname = basename.rsplit('.', 1)[0]
filename=jobname+'.xyz'
print(filename)
atoms.write(filename)
print(f"Written: {jobname}.xyz")
