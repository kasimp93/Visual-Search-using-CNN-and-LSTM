#!/bin/bash

# Load modules
module load cuda/8.0
module load cudnn/5.1
module load python/2.7.13
module load tensorflow/r1.0_python-2.7.13
module load nltk
module load java/1.8.0_92
module load bazel/0.5.2

export CUDA_VISIBLE_DEVICES=""

