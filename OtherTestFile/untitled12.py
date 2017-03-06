# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 19:09:34 2017

@author: LLL
"""

try:
    import tensorflow as tf
except:
    import os
    os.system('pip install tensorflow')
finally:
    import xlrd
    import tensorflow as tf
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import time

    

IRIS_TRAINING = "iris_training.csv"
IRIS_TEST = "iris_test.csv"
tf.contrib.learn.datasets.base.load_csv_with_header(
    filename=IRIS_TRAINING,
    target_dtype=np.int,
    features_dtype=np.float32)