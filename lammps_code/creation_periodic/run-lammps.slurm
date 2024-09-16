#!/bin/bash
#SBATCH --job-name=test
#SBATCH --nodes=2                # 5 nodes
#SBATCH --ntasks-per-node=8     # 20 Number of tasks to be invoked on each node
#SBATCH --cpus-per-task=1        # Threads per task(=1) for pure MPI
#SBATCH --time=3:00:00             #Run time in hh:mm:ss
#sbatch --partition=testing      #sbatch --partition=batch
#SBATCH --error=job.%J.out
#SBATCH --output=job.%J.out

echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running on $SLURM_NPROCS processors."
echo "Job id is $SLURM_JOBID"
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

#Loading conda to the nodes
module load gcc miniconda3
source $CONDA_PROFILE/conda.sh
conda activate lammps_oct
export PATH=$CONDA_PREFIX/bin:$PATH
#Loading MPI Library
module load gcc/9.2.0 openmpi/3.1.3
mpirun -np 16 lmp_mpi -in final_creation.in
#srun lmp_serial < main.in

echo "Program finished with exit code $? at: `date`"
