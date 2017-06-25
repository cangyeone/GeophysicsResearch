import tensorflow as tf

class WaveIdentify():
    def __init__(self):
        self.conv_shape={
            "conv_layer1":[[4,3,8],[8]],
            "conv_layer2":[[4,8,16],[16]],
            "conv_layer3":[[4,16,32],[32]],
            "conv_layer4":[[4,32,32],[32]],
            "conv_layer5":[[4,32,16],[16]],
            "conv_layer6":[[4,16,16],[16]]
        }
        self.full_shape={
            "full_layer1":[[100,30],[30]],
            "full_layer2":[[30,1],[1]]
        }
        self.sess=tf.Session()
    def def_struct(self):
        with tf.variable_scope("input_layer"):
            data=tf.placeholder(tf.float32,[50,10000,3])
            vali=tf.placeholder(tf.float32,[50,1])
        for c_l in self.conv_shape:
            with tf.variable_scope(c_l):
                data=self.conv_relu(data,self.conv_shape[c_l][0],self.conv_shape[c_l][1])
        with tf.name_scope("flaton"):
            data=data.reshape(data,[50,-1])
        for f_l in self.full_shape:
            with tf.variable_scope(f_l):
                data=self.full_connect(data,self.full_shape[f_l][0],self.full_shape[f_l][1])
        with tf.name_scope("train"):
            for_valid=tf.reduce_mean(tf.square(data-vali))
            self.train_step = tf.train.AdamOptimizer(1e-2).minimize(for_valid)
            self.vali_data=data
    def conv_relu(self,data,weigh_shape,bias_shape):
        weight = tf.get_variable("conv_weight",weigh_shape,initializer=tf.random_normal_initializer())
        biases = tf.get_variable("conv_bias",bias_shape,initializer=tf.constant_initializer(0.0))
        conv = tf.nn.conv1d(data,weight,stride=[1,1,1],padding='SAME')
        return tf.nn.relu(conv+biases)
    def full_connect(self,data,weight_shape,bias_shape):
        weight = tf.get_variable("full_connect_weight",weigh_shape,initializer=tf.random_normal_initializer())
        biases = tf.get_variable("full_connect_bias",bias_shape,initializer=tf.constant_initializer(0.0))
        return tf.matmul(data,weight)+biases
    def train(self,data,vali):
        self.sess.run(tf.global_variables_initializer())
        self.sess.run(self.train_step,feed_dict={data:data,vali:vali})
    def valid(self,data):
        return self.sess.run(self.vali_data)
        

    