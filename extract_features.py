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

import tensorflow as tf
import numpy as np

from google.protobuf import text_format
from tensorflow.python.platform import app
from delf import delf_config_pb2
from delf import feature_extractor
from delf import feature_io



from keras.preprocessing import image as kimage
from argparse import ArgumentParser
import os.path

cmd_args = None

# Extension of feature files.
_DELF_EXT = '.delf'

# Pace to report extraction log.
_STATUS_CHECK_ITERATIONS = 100

# checking the file path
def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle

# Arguments for the file
parser = ArgumentParser(description="Input Images")

parser.add_argument("-i", dest="filename", required=True,
                    help="input file with two matrices", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))

parser.add_argument("-o", dest="gpu_name", required=True,
                    help="input file with two matrices", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))
      

# Getting file name
args = parser.parse_args().filename.name
args1 = parser.parse_args().gpu_name.name

print("GOT the file to work --", args1)

print("Opened the file for reading : ",args)

with open(args,"r") as f:
   input_images= f.readlines()

num_images = len(input_images)

print("FOUND %d images...", num_images)

tf.logging.set_verbosity(tf.logging.INFO)

with tf.Graph().as_default():
  
  with tf.Session() as sess:
    
    modelsssss = feature_extractor.BuildModel()

    x = tf.placeholder(tf.float32, [224,224,3])
    
    feature_map, feature_map1 = modelsssss(x, False, False)

    print("Returning the features", feature_map1)

    # Initialize variables.
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    f = open(args1,'ab')

    for i in range(0,num_images):
      # # Get next image.
      img_path = '/../../../../../../media/sdi/dinesh/Landmark/trainimagesR/'
      img_path += input_images[i].rstrip()
      
      image_tf = kimage.load_img(img_path, target_size=(224, 224))
      image_tf = kimage.img_to_array(image_tf)
      imagetest = image_tf
      print("EXTRACTING FOR ", i + 1, " IMAGE")

      (feature_map_out, feature_map1_out) = sess.run([feature_map, feature_map1], 
      feed_dict ={
                x:imagetest
      })
      
      array_feature_map1_out =  np.expand_dims(feature_map1_out, axis=0)

    #   array_feature_map1_out_precise = []
    #   for element in feature_map1_out:
    #       array_feature_map1_out_precise.append(round(element, 8))

      array_feature_map1_out_precise = np.round(array_feature_map1_out, 8)
    
      # array_feature_map1_out_precise = np.expand_dims(array_feature_map1_out_precise, axis = 0)
      np.savetxt(f, array_feature_map1_out_precise, '%.8g')
     
    print("COMPLETED OUTPUT IN test_images.csv")

    