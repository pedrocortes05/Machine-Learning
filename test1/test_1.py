import math
import numpy as np
#import functions.py
import seaborn as sns
from numpy import random
from matplotlib import animation
import matplotlib.pyplot as plt


class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        self.weights1 = randomMatrix(self.hidden_nodes, self.input_nodes)
        self.weights2 = randomMatrix(self.output_nodes, self.hidden_nodes)

        self.bias1 = randomMatrix(self.hidden_nodes, 1)
        self.bias2 = randomMatrix(self.output_nodes, 1)

        self.learning_rate = 0.1
        self.error = np.zeros(shape=(1,1))
        self.error = randomMatrix(1, 1)

    def feed_forward(self, inputs):
        layer2 = map(add(multiply(self.weights1, inputs), self.bias1), sigmoid)
        output = map(add(multiply(self.weights2, layer2), self.bias2), sigmoid)
        return output

    def train(self, inputs, targets):
        #outputs = self.feed_forward(inputs)

        layer2 = map(add(multiply(self.weights1, inputs), self.bias1), sigmoid)
        output = map(add(multiply(self.weights2, layer2), self.bias2), sigmoid)
        outputs = output

        output_errors = subtract(targets, outputs)
        hidden_errors = multiply(transpose(self.weights2), output_errors)
        self.error = output_errors

        # Output - Hidden
        output_gradients = self.learning_rate * multiply2(map(outputs, gradient), output_errors)
        delta_weights2 = multiply(output_gradients, transpose(layer2))

        # Add deltas to original bias and weights
        self.weights2 = add(self.weights2, delta_weights2)
        self.bias2 = add(self.bias2, output_gradients)

        # Hidden - Input
        hidden_gradients = self.learning_rate * multiply2(map(layer2, gradient), hidden_errors)
        delta_weights1 = multiply(hidden_gradients, transpose(inputs))

        # Add deltas to original bias and weights
        self.weights1 = add(self.weights1, delta_weights1)
        self.bias1 = add(self.bias1, hidden_gradients)
        


def randomMatrix(row, col):
    arr = np.zeros(shape=(row,col))
    for row in range(arr.shape[0]):
        for col in range(arr.shape[1]):
            arr[row, col] = random.random() * 2 - 1
    return arr

def transpose(matrix):
    result = np.zeros(shape=(matrix.shape[1], matrix.shape[0]))
    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            result[col, row] = matrix[row, col]
    return result

def multiply(a, b):
    if a.shape[1] == b.shape[0]:
        result = np.zeros(shape=(a.shape[0], b.shape[1]))
        for row in range(result.shape[0]):
            for col in range(result.shape[1]):
                for i in range(a.shape[1]):
                    result[row, col] += a[row, i] * b[i, col]
        return result
    else:
        print("cant multply!!!!!!!!!!!!!!!!!!!")

def multiply2(a, b):
    if a.shape == b.shape:
        result = np.zeros(shape=a.shape)
        for row in range(result.shape[0]):
            for col in range(result.shape[1]):
                result[row, col] = a[row, col] * b[row, col]
        return result
    else:
        print("cant multiply!!!!!!!!!!!!!!!!!!!!!!")

def add(a, b):
    if a.shape == b.shape:
        result = np.zeros(shape=(a.shape))
        for row in range(result.shape[0]):
            for col in range(result.shape[1]):
                result[row, col] = a[row, col] + b[row, col]
        return result

def subtract(a, b):
    if a.shape == b.shape:
        result = np.zeros(shape=(a.shape))
        for row in range(result.shape[0]):
            for col in range(result.shape[1]):
                result[row, col] = a[row, col] - b[row, col]
        return result

def map(matrix, myfunc):
    result = np.zeros(shape=(matrix.shape))
    for row in range(result.shape[0]):
        for col in range(result.shape[1]):
            result[row, col] = myfunc(matrix[row, col])
    return result

def sigmoid(n):
    return 1 / (1 + math.exp(-n))

def gradient(n):
    return n * (1 - n)


training_data = {
    "1" : {
        "inputs": np.array([[1], [0]]),
        "targets": np.array([[1]])
    },
    "2" : {
        "inputs": np.array([[0], [1]]),
        "targets": np.array([[1]])
    },
    "3" : {
        "inputs": np.array([[1], [1]]),
        "targets": np.array([[0]])
    },
    "4" : {
        "inputs": np.array([[0], [0]]),
        "targets": np.array([[0]])
    }
}

def init():
    sns.heatmap(nn.weights1, vmin=-1, vmax=1, annot=True, cbar=True)
    print('hi')


def animate(i):
    for x in range(100):
        for data in training_data:
            nn.train(training_data[data]["inputs"], training_data[data]["targets"])
    print(nn.error, "Error")
    sns.heatmap(nn.error, vmin=-1, vmax=1, annot=False, cbar=False)

nn = NeuralNetwork(2, 2, 1)
fig = plt.figure()
anim = animation.FuncAnimation(fig, animate, init_func=init, interval=10)

plt.show()
#for x in range(1000):
#    for data in training_data:
#        nn.train(training_data[data]["inputs"], training_data[data]["targets"])
#        print(x)


print(nn.feed_forward(np.array([[1], [0]])))
print(nn.feed_forward(np.array([[0], [1]])))
print(nn.feed_forward(np.array([[1], [1]])))
print(nn.feed_forward(np.array([[0], [0]])))