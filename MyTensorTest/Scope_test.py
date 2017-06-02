import tensorflow as tf
import numpy as np


def conv_relu(input, kernel_shape, bias_shape):
    # Create variable named "weights".
    weights = tf.get_variable("weights", kernel_shape,
        initializer=tf.random_normal_initializer(),dtype=tf.float64)
    # Create variable named "biases".
    biases = tf.get_variable("biases", bias_shape,
        initializer=tf.constant_initializer(0.0),dtype=tf.float64)
    conv = tf.nn.conv2d(input, weights,
        strides=[1, 1, 1, 1], padding='SAME')
    return tf.nn.relu(conv + biases)

def my_image_filter(input_images):
    with tf.variable_scope("conv1"):
        # Variables created here will be named "conv1/weights", "conv1/biases".
        relu1 = conv_relu(input_images, [5, 5, 1, 32], [32])
    with tf.variable_scope("conv2"):
        # Variables created here will be named "conv2/weights", "conv2/biases".
        return conv_relu(relu1, [5, 5, 32, 32], [32])

with tf.variable_scope("image_filters") as scope:
    result1 = my_image_filter(np.ones([1,100,100,1]))
    scope.reuse_variables()
    result2 = my_image_filter(np.ones([1,100,100,1]))

print(result1.name)
print(result2.name)
# Raises ValueError(... conv1/weights already exists ...)