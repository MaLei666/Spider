# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from sklearn.metrics import confusion_matrix
from tensorflow.examples.tutorials.mnist import input_data

# data = input_data.read_data_sets("/home/py/captcha/MNIST/", one_hot=True)
data = input_data.read_data_sets("E:/MNIST/", one_hot=True)