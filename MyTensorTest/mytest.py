import tensorflow as tf
import numpy as np

lstm_size=5
batch_size=5
lstm = tf.contrib.rnn.BasicLSTMCell(lstm_size)
print([batch_size,lstm.state_size])
# Initial state of the LSTM memory.
state_c = tf.constant(np.zeros([lstm.state_size[0]]))
state_h = tf.constant(np.zeros([lstm.state_size[1]]))
state = tf.zeros([batch_size])
#probabilities = []
#loss = 0.0
current_batch_of_words=np.ones([1,2,3,4,5])
output, state = lstm(current_batch_of_words, (state_c,state_h))

    # The LSTM output can be used to make next word predictions
#logits = tf.matmul(output, softmax_w) + softmax_b
init=tf.initialize_all_variables()
sess=tf.Session()
sess.run(init)
#print(sess.run(state))