# Copyright (c) 2023 Dmitry Rogozhkin
# SPDX-License-Identifier: Apache-2.0

# See: https://www.iree.dev/guides/ml-frameworks/tensorflow/#missing-serving-signature-in-savedmodel

import argparse
import tensorflow.compat.v2 as tf

argParser = argparse.ArgumentParser(
  description='Resaves input model with the serving signature.',
  )
argParser.add_argument('-i', help='path to intput model', required=True)
argParser.add_argument('-o', help='path for output model', required=True)

args = argParser.parse_args()

model = tf.saved_model.load(args.i)
call = model.__call__.get_concrete_function(
  tf.TensorSpec([1, 224, 224, 3], tf.float32))
signatures = {'predict': call}
tf.saved_model.save(model, args.o, signatures=signatures)

