import  os
import  tensorflow as tf
from    tensorflow import keras
from    tensorflow.keras import layers, optimizers, datasets
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

def load_minist_data(path='mnist.npz'):
  """Loads the MNIST dataset.

  Arguments:
      path: path where to cache the dataset locally
          (relative to ~/.keras/datasets).

  Returns:
      Tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.

  License:
      Yann LeCun and Corinna Cortes hold the copyright of MNIST dataset,
      which is a derivative work from original NIST datasets.
      MNIST dataset is made available under the terms of the
      [Creative Commons Attribution-Share Alike 3.0 license.](
      https://creativecommons.org/licenses/by-sa/3.0/)
  """

  path = "D:/E_Class/deep_learning/project_2/mnist.npz"
  with np.load(path) as f:
    x_train, y_train = f['x_train'], f['y_train']
    x_test, y_test = f['x_test'], f['y_test']

    return (x_train, y_train), (x_test, y_test)

#Load MNIST DATA from file "mnist.npz" , please add your code bellow:
(x, y), (x_val, y_val) = load_minist_data()
#Convert data to tensor, and then make normalization for hand writing digit 
x = tf.convert_to_tensor(x, dtype=tf.float32) / 255.
#Convert data to tensor, please add your code bellow:
y = tf.convert_to_tensor(y, dtype=tf.int32)
#Here, y is a int value, please transfer it to one hot coding with "depth=10" using tesorflow command
#, please add your code bellow:
y = tf.one_hot(y, depth=10)
print(x.shape, y.shape)
train_dataset = tf.data.Dataset.from_tensor_slices((x, y))
#Please set the batch size, for instance 100 or 200, please add your code bellow:
train_dataset = train_dataset.batch(200)

#请按照上面train_dataset的数据准备方法（tf.data.Dataset.from_tensor_slices),准备test_dataset,
#Please add your code bellow:
x_val = tf.convert_to_tensor(x_val, dtype=tf.float32) / 255.
y_val = tf.convert_to_tensor(y_val, dtype=tf.int32)
y_val = tf.one_hot(y_val, depth=10)
test_dataset = tf.data.Dataset.from_tensor_slices((x_val, y_val))

test_dataset = test_dataset.batch(200)

 

#Bellow is defination of hidden-layer in network, you have the chice to make dicision about the number 
# of neurons, the activation is 'relu', please add your code bellow:
model = keras.Sequential([

    layers.Dense(256, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')])

optimizer = optimizers.SGD(learning_rate=0.001)


def train_epoch(epoch):

    # Step4.loop
    for step, (x, y) in enumerate(train_dataset):


        with tf.GradientTape() as tape:
            # [b, 28, 28] => [b, 784]
            x = tf.reshape(x, (-1, 28*28))
            # Step1. compute output
            # [b, 784] => [b, 10]
            out = model(x)
            # Step2. compute loss
            loss = tf.reduce_sum(tf.square(out - y)) / x.shape[0]

        # Step3. optimize and update w1, w2, w3, b1, b2, b3
        grads = tape.gradient(loss, model.trainable_variables)
        # w' = w - lr * grad
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        if step % 100 == 0:
            print(epoch, step, 'loss:', loss.numpy())

#在训练完成后，请利用已经得到的model验证在测试集上的结果，请仿照上面training_epoch的在下面写出你的具体测试代码
#并输出测试结果（预测值，groud truth），注意只是测试不需要计算loss和计算梯度
def test():
    total = 0
    correct = 0

    for x, y in test_dataset:
        x = tf.reshape(x, (-1, 28 * 28))
        out = model(x)
        pred = tf.argmax(out, axis=1)
        truth = tf.argmax(y, axis=1)

        correct += int(tf.reduce_sum(tf.cast(tf.equal(pred, truth), tf.int32)).numpy())
        total += int(x.shape[0])

        print('predict:', pred[:10].numpy(), 'ground truth:', truth[:10].numpy())

    print('test accuracy:', correct / total)


def train():

    for epoch in range(30):

        train_epoch(epoch)
#30个epoch之后调用test_epoch,
    test()

#如果你学有余力，请利用我们给的hand writing digit image测试用例，试一试你训练的model（选做）
#注意你需要利用Python先读入test.jpg图像，然后把它转换为灰度图像，然后将图像由28*28转化为784长度的向量，
#然后送入模型，最后输出判别结果。
if __name__ == '__main__':
    train()