#!/bin/bash
#
#SBATCH --job-name=dummyParallel
#SBATCH --output=log.%x
#
#SBATCH --ntasks=16
#SBATCH --time=0-12:00:00
#SBATCH --partition=preemptible
#SBATCH --mem=90G
#SBATCH --ear=off

echo "#############################"
echo "User:" $USER
echo "Submit time:" $(squeue -u $USER -o '%30j %20V' | \
    grep -e $SLURM_JOB_NAME | awk '{print $2}')
echo "Launch time:" `date +"%Y-%m-%dT%T"`
echo "Host:" `hostname`
echo "Directory:" `pwd`
echo "SLURM_JOBID:" $SLURM_JOBID
echo "SLURM_JOB_NAME:" $SLURM_JOB_NAME
echo "SLURM_SUBMIT_DIR:" $SLURM_SUBMIT_DIR
echo "SLURM_JOB_NODELIST:" $SLURM_JOB_NODELIST
echo "#############################"

#- Ensure only owner can read the output
umask 0077

export SLURM_COMP_VERBOSE=3
export SLURM_LOADER_VERBOSE=3

#- User input
np=16

module purge
module load openmpi/4.1.1/gcc/11.2.0
module load mpi4py/3.1.1/mpi/openmpi/4.1.1

start=`date +%s.%N`

#--------------------------------------------------

echo "Generating dummy data ..."
python dummyDataGenerator.py 
echo "=============================="
echo "Running serial script ..."
python getStdDev.serial.py # > log.runscript.serial 2>&1
echo "=============================="
echo "Running parallel script ..."
mpirun -np $np python getStdDev.parallel.py # > log.runscript.parallel 2>&1

#--------------------------------------------------

end=`date +%s.%N`

echo "=============================="
echo "DONE!"
echo "Runtime:" $( echo "$end - $start" | bc -l )

# ----------------------------------------------------------------- end-of-file