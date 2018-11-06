import caffe
import cv2
import numpy as np

import sys
sys.path.append('/home/lc/keras2caffe')

import SqueezeNet

import keras2caffe

#converting
keras_model = SqueezeNet()

keras2caffe.convert(keras_model, 'SqueezeNet.prototxt', 'SqueezeNet.caffemodel')

#testing the model

caffe.set_mode_gpu()
net  = caffe.Net('SqueezeNet.prototxt', 'SqueezeNet.caffemodel', caffe.TEST)

img = cv2.imread('bear.jpg')

img = cv2.resize(img, (227, 227))
img = img[...,::-1]  #RGB 2 BGR

data = np.array(img, dtype=np.float32)
data = data.transpose((2, 0, 1))
data.shape = (1,) + data.shape

data -= 128

net.blobs['data'].data[...] = data

out = net.forward()
preds = out['global_average_pooling2d_1']

classes = eval(open('class_names.txt', 'r').read())
print("Class is: " + classes[np.argmax(preds)])
print("Certainty is: " + str(preds[0][np.argmax(preds)]))



