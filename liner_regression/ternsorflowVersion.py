import tensorflow as tf
W = tf.Variable(tf.zeros(2),name="weights")
b = tf.Variable(0.0,name = "bias")
x = [1,2,3,4,5]
y = tuple(map(lambda i: i * 100.0 + 10 ,x))

def inference(X):
    return tf.add(W[0] * X,b)
    
def loss(X,Y):
    Y_predicted = inference(X)
    return tf.reduce_sum(tf.squared_difference(Y,Y_predicted))
def inputs():
    return tf.to_float(x),tf.to_float(y)
def train(totalLoss):
    learnning_rate = 0.01
    return tf.train.GradientDescentOptimizer(learnning_rate).minimize(total_loss)
def evaluate(sess,X,Y):
    print(sess.run(loss(X,Y)),sess.run(inference([[1.0,1.0]])))
saver = tf.train.Saver()
with tf.Session() as sess:
    tf.initialize_all_variables().run()
    X,Y = inputs()
    total_loss = loss(X,Y)
    train_op = train(total_loss)
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess = sess,coord=coord)
    trainning_steps = 100000
    for step in range(trainning_steps):
        sess.run([train_op])
        if step % 1000 == 0:
            evaluate(sess,X,Y)                        
            print("Loss:",sess.run([total_loss]),sess.run([W,b]))
            saver.save(sess,"output/mymodel",global_step=step)
    saver.save(sess,"output/mymodel",global_step=trainning_steps)    
    evaluate(sess,X,Y)
    coord.request_stop()
    coord.join(threads)
    sess.close()
    pass