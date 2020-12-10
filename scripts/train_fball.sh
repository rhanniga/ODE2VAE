#!/bin/bash
python train.py \
  --task fball \
  --data_root data \
  --q 25 \
  --Hf 100 \
  --amort_len 3 \
  --batch_size 10 \
  --activation_fn "relu" \
  --eta 0.0008 \
  --num_epoch 100