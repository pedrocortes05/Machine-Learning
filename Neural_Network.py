import math
import numpy as np
from numpy import random
from copy import deepcopy

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
        layer2 = map((np.dot(self.weights1, inputs) + self.bias1), sigmoid)
        output = map((np.dot(self.weights2, layer2) + self.bias2), sigmoid)
        return output

    def train(self, inputs, targets):
        layer2 = map((np.dot(self.weights1, inputs) + self.bias1), sigmoid)
        output = map((np.dot(self.weights2, layer2) + self.bias2), sigmoid)
        outputs = output

        output_errors = targets - outputs
        hidden_errors = np.dot(transpose(self.weights2), output_errors)
        self.error = output_errors

        # Output - Hidden
        output_gradients = self.learning_rate * (map(outputs, gradient) * output_errors)
        delta_weights2 = np.dot(output_gradients, transpose(layer2))

        # Add deltas to original bias and weights
        self.weights2 = self.weights2 + delta_weights2
        self.bias2 = self.bias2 + output_gradients

        # Hidden - Input
        hidden_gradients = self.learning_rate * (map(layer2, gradient) * hidden_errors)
        delta_weights1 = np.dot(hidden_gradients, transpose(inputs))

        # Add deltas to original bias and weights
        self.weights1 = self.weights1 + delta_weights1
        self.bias1 = self.bias1 + hidden_gradients
    

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

def map(matrix, myfunc):
    result = np.zeros(shape=(matrix.shape))
    for row in range(result.shape[0]):
        for col in range(result.shape[1]):
            result[row, col] = myfunc(matrix[row, col])
    return result

def mutate():
    print()

def sigmoid(n):
    return 1 / (1 + math.exp(-n))

def gradient(n):
    return n * (1 - n)