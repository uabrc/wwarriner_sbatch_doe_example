#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --partition=express
#SBATCH --output=sbatch_%A.log
#SBATCH --error=sbatch_%A.log

ml Anaconda3
conda activate sbatch
python -u sbatch.py
