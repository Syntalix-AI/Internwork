from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Flatten, Dropout, BatchNormalization



#custom Activation Function
import tensorflow as tf

def custom_activation_1(x):
    sigmoid = tf.nn.sigmoid(x)
    relu = tf.nn.relu(x)
    return (sigmoid + relu) / 2

def custom_activation_2(x):
    sigmoid = tf.nn.sigmoid(x)
    relu = tf.nn.relu(x)
    tanh = tf.nn.tanh(x)
    leaky_relu = tf.nn.leaky_relu(x)
    return (0.05*sigmoid + 0.8*relu + 0.05*tanh + 0.1*leaky_relu)


def custom_activation_3(x):
    sigmoid = tf.nn.sigmoid(x)
    relu = tf.nn.relu(x)
    tanh = tf.nn.tanh(x)
    leaky_relu = tf.nn.leaky_relu(x)
    return (sigmoid + relu + tanh + leaky_relu) / 4

def custom_activation_4(x):
    sigmoid = tf.nn.sigmoid(x)
    relu = tf.nn.relu(x)
    tanh = tf.nn.tanh(x)
    leaky_relu = tf.nn.leaky_relu(x)
    return sigmoid


def custom_activation_5(x):
    sigmoid = tf.nn.sigmoid(x)
    relu = tf.nn.relu(x)
    tanh = tf.nn.tanh(x)
    leaky_relu = tf.nn.leaky_relu(x)
    return leaky_relu

def custom_activation_6(x):
    sigmoid = tf.nn.sigmoid(x)
    relu = tf.nn.relu(x)
    tanh = tf.nn.tanh(x)
    leaky_relu = tf.nn.leaky_relu(x)
    return relu


def custom_activation_7(x):
    sigmoid = tf.nn.sigmoid(x)
    relu = tf.nn.relu(x)
    tanh = tf.nn.tanh(x)
    leaky_relu = tf.nn.leaky_relu(x)
    return tanh












# Load and preprocess MNIST data
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255
x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Build the model
model = Sequential()
model.add(Dropout(0.5))
model.add(Flatten(input_shape=(28, 28, 1)))  # Input layer
model.add(Dense(128, activation=custom_activation_2))  # Custom activation function in hidden layer
model.add(Dense(10, activation='softmax'))  # Output layer

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# training the model
model.fit(x_train, y_train, epochs=10, batch_size=32, validation_split=0.2)


# Evaluate the model
test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
print(f'Test accuracy: {test_accuracy}')
