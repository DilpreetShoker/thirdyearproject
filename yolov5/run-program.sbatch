#!/bin/bash
#
#SBATCH --job-name=cricket # Job name for tracking
#SBATCH --partition=eagle  # Partition you wish to use (see above for list)
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6     # Number of CPU threads used by your job
#SBATCH --gres=gpu:1           # Number of GPUs to use 
#SBATCH --time=2-00:00:00      # Job time limit set to 2 days (48 hours)
#
#SBATCH --mail-type=END,FAIL,TIME_LIMIT_80 # Events to send email on, remove if you don't want this
#SBATCH --output=joboutput_%j.out # Standard out from your job
#SBATCH --error=joboutput_%j.err  # Standard error from your job

## Initialisation ##

## Execute your program(s) ##

srun python3.11 train.py --data ../dataset1/data.yaml --weights  yolov5l.pt --img 640 --epochs 30 --batch-size 20 --name dataset1_e20_b24
