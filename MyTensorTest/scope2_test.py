import tensorflow as tf
import numpy as np

with tf.variable_scope("foo"):
    with tf.name_scope("bar"):
        v = tf.get_variable("v", [1])
        x = 1.0 + v
print(v.name == "foo/v:0"
assert x.op.name == "foo/bar/add"

