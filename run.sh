#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --partition=express
#SBATCH --output=%j_%4a.log
#SBATCH --error=%j_%4a.log
#SBATCH --array=0-26%4

ml Anaconda3
conda activate test_env
python -u payload.py black_box.sh doe.csv %a
