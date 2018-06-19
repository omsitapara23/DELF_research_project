# Copyright 2017 The TensorFlow Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Extracts DELF features from a list of images, saving them to file.

The images must be in JPG format. The program checks if descriptors already
exist, and skips computation for those.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import sys
import time
import numpy as np

import tensorflow as tf

from google.protobuf import text_format
from tensorflow.python.platform import app
from delf import delf_config_pb2
from delf import feature_extractor
from delf import feature_io

cmd_args = None

# Extension of feature files.
_DELF_EXT = '.delf'

# Pace to report extraction log.
_STATUS_CHECK_ITERATIONS = 100

# feature_map=None
# feature_map1=None

def _ReadImageList(list_path):
  """Helper function to read image paths.

  Args:
    list_path: Path to list of images, one image path per line.

  Returns:
    image_paths: List of image paths.
  """
  with tf.gfile.GFile(list_path, 'r') as f:
    image_paths = f.readlines()
  image_paths = [entry.rstrip() for entry in image_paths]
  return image_paths


def main(unused_argv):
  tf.logging.set_verbosity(tf.logging.INFO)

  # Read list of images.
  tf.logging.info('Reading list of images...')
  image_paths = _ReadImageList(cmd_args.list_images_path)
  num_images = len(image_paths)
  tf.logging.info('done! Found %d images', num_images)

  # Parse DelfConfig proto.
  config = delf_config_pb2.DelfConfig()
  with tf.gfile.FastGFile(cmd_args.config_path, 'r') as f:
    text_format.Merge(f.read(), config)

  # Create output directory if necessary.
  if not os.path.exists(cmd_args.output_dir):
    os.makedirs(cmd_args.output_dir)

  with tf.Graph().as_default():
      filename_queue = tf.train.string_input_producer(image_paths, shuffle=False)
      print("PRINTING THE fileNAME QUEUE", filename_queue)
      reader = tf.WholeFileReader()
      print("PRINTING THE reader", reader)
      _, value = reader.read(filename_queue)
      print("PRINTING the VALUE", value)
      image_data = 'data/oxford5k_images/hertford_000057.jpg'
      test_image_tf1 = tf.read_file(image_data)
      image_tf1 = tf.image.decode_jpeg(value, channels=3)
      image_tf1 = tf.image.resize_image_with_crop_or_pad(image_tf1,100,100)
      #image_tf1 = np.random.randn(100,100,3)
      print("THE IMAGE", image_tf1)
      """
      ADDED FOR CHECKING PURPOSE ONLY
      """
      imagetest = image_tf1
      imagetest = tf.expand_dims(imagetest, 0)
      print("size of tensor === ",imagetest)
      print("THE IMAGE FORMED", imagetest)
      print("MAKING FIRST FUNCTION")
      modelsssss = feature_extractor.BuildModel('resnet_v1_50/block3', 'softplus', 'use_l2_normalized_feature',1)
      print("CALLING THE MODEL")
      with tf.Session() as sess:
          # Initialize variables.
          init_op = tf.global_variables_initializer()
          print("SHOWING OPERATION", init_op)
          tf.logging.info('Starting session...')
          sess.run(init_op)
          tf.logging.info('Starting to load the models to be used...')
          feature_map, feature_map1 = modelsssss(imagetest, False, False)
          sess.run([feature_map,feature_map1])
          print(feature_map)
          print(feature_map1)
      print("CAME BACK TO ORIGINAL")

    #   print(feature_map)
    #   print(feature_map1)
      # print(sess.run(feature_map))
      # print(sess.run(feature_map1))
    #   return feature_map, feature_map1

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.register('type', 'bool', lambda v: v.lower() == 'true')
  parser.add_argument(
      '--config_path',
      type=str,
      default='delf_config_example.pbtxt',
      help="""
      Path to DelfConfig proto text file with configuration to be used for DELF
      extraction.
      """)
  parser.add_argument(
      '--list_images_path',
      type=str,
      default='list_images.txt',
      help="""
      Path to list of images whose DELF features will be extracted.
      """)
  parser.add_argument(
      '--output_dir',
      type=str,
      default='test_features',
      help="""
      Directory where DELF features will be written to. Each image's features
      will be written to a file with same name, and extension replaced by .delf.
      """)
  cmd_args, unparsed = parser.parse_known_args()
  app.run(main=main, argv=[sys.argv[0]] + unparsed)
