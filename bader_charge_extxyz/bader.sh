####Script to automatically run bader charge calculation from a finished scf run
####Followed by postprocessing to store the charges as an extxyz file (using ASE)
####Usage: bash bader.sh <path to scf input file>
#Automatically detects the prefix and outdir for the pp.x computations

prefix=$(grep prefix $1 | awk '{print $NF}')
out=$(grep outdir $1 )
outdir=${out#*=}
name="$1"
jobname=$(echo ${name%.*})


cat > val.in << EOF
&INPUTPP
  prefix = $prefix
  outdir = $outdir
  filplot = 'val.charge'
  plot_num = 0
/
&PLOT
  iflag = 3
  nfile=1
  output_format = 6
  fileout = 'val.cube'
/
EOF

mpirun pp.x < val.in > val.out

cat > all.in << EOF
&INPUTPP
  prefix = $prefix
  outdir = $outdir
  filplot = 'all.charge'
  plot_num = 0
/
&PLOT
  iflag = 3
  nfile=1
  output_format = 6
  fileout = 'all.cube'
/
EOF

mpirun pp.x < all.in > all.out

/home/a_thomas.iitr/SWs/bader/bader val.cube -ref all.cube   ###Adjust the path to your bader executable
rm *charge *cube

python conv_charges.py "$1"
