import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import animation
from Neural_Network import *


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

# Simulation Seaborn
def init():
    sns.heatmap(nn.weights1, vmin=-1, vmax=1, annot=False, cbar=True)

def animate(i):
    for x in range(100):
        for data in training_data:
            nn.train(training_data[data]["inputs"], training_data[data]["targets"])
    print(nn.error)
    sns.heatmap(nn.weights1, vmin=-1, vmax=1, annot=False, cbar=False)


nn = NeuralNetwork(2, 2, 1)
fig = plt.figure()
anim = animation.FuncAnimation(fig, animate, init_func=init, interval=10)

plt.show()

nn2 = deepcopy(nn)

print(nn.feed_forward(np.array([[1], [0]])), "Correct answer is: 1")
print(nn.feed_forward(np.array([[0], [1]])), "Correct answer is: 1")
print(nn.feed_forward(np.array([[1], [1]])), "Correct answer is: 0")
print(nn.feed_forward(np.array([[0], [0]])), "Correct answer is: 0")