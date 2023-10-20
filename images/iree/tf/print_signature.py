# Copyright (c) 2023 Dmitry Rogozhkin
# SPDX-License-Identifier: Apache-2.0

import argparse
import tensorflow.compat.v2 as tf

argParser = argparse.ArgumentParser(
  description='Prints model serving signature.',
  )
argParser.add_argument('-i', help='path to intput model', required=True)

args = argParser.parse_args()

model = tf.saved_model.load(args.i)
print(list(model.signatures.keys()))

