ml Anaconda3
conda activate test_env
python -u payload.py ./black_box.sh doe.csv "$SLURM_ARRAY_TASK_ID"
