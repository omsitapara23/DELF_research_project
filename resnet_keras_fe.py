from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.models import Model
import numpy as np

from argparse import ArgumentParser
import os.path

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

# Getting file name
args = parser.parse_args().filename.name

print("Opened the file for reading : ",args)

with open(args,"r") as f:
   input_images= f.readlines()

numlength = len(input_images)

print("FOUND %d images...", numlength)


base_model = ResNet50(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('bn4f_branch2c').output)

for i in range(0, numlength) :
    img_path = input_images[i].rstrip()
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    block4_pool_features = model.predict(x)
    vec_block4_pool_features = block4_pool_features.flatten()
    print("FOR IMAGE i", i)
    print(vec_block4_pool_features)
    array_block4_pool_features =  np.expand_dims(vec_block4_pool_features, axis=0)
    if i == 0 :
        out_matrix = array_block4_pool_features
    else :
        out_matrix = np.append(out_matrix,array_block4_pool_features,axis=0)

np.savetxt('out.csv', out_matrix)







