import os
from typing import List, Tuple
import numpy as np
from tensorflow_core.python.keras.datasets import mnist
from definitions import DATA_PATH

LOG_SOURCE: str = "DATA_SPLIT"
num_classes: int = 10
img_size: int = 28 * 28

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train: np.array = x_train.reshape(x_train.shape[0], img_size, 1)
x_test: np.array = x_test.reshape(x_test.shape[0], img_size, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255  # normalize
x_test /= 255  # normalize
print("[%s] splitting %i train samples" % (LOG_SOURCE, x_train.shape[0]))
print("[%s] splitting %i test samples" % (LOG_SOURCE, x_test.shape[0]))

separated_train_data: List[Tuple[np.array or List[any], np.array or List[any]]] = [([], []) for _ in range(num_classes)]
separated_test_data: List[Tuple[np.array or List[any], np.array or List[any]]] = [([], []) for _ in range(num_classes)]

for result, image in zip(y_train, x_train):
    separated_train_data[result][0].append(image)
    separated_train_data[result][1].append(result)

for result, image in zip(y_test, x_test):
    separated_test_data[result][0].append(image)
    separated_test_data[result][1].append(result)

for i in range(num_classes):
    separated_train_data[i] = (np.array(separated_train_data[i][0]).reshape([-1, img_size, 1]),
                               np.array(separated_train_data[i][1]).reshape([-1, 1]))
    separated_test_data[i] = (np.array(separated_test_data[i][0]).reshape([-1, img_size, 1]),
                              np.array(separated_test_data[i][1]).reshape([-1, 1]))
    print("[%s] %i train samples for class #%i" % (LOG_SOURCE, separated_train_data[i][0].shape[0], i))
    print("[%s] %i test samples for class #%i" % (LOG_SOURCE, separated_test_data[i][0].shape[0], i))

data_path: str = DATA_PATH + "mnist"
if not os.path.exists(data_path):
    os.makedirs(data_path)

np.savez("%s/mnist_train_split" % data_path, separated_train_data)
np.savez("%s/mnist_test_split" % data_path, separated_test_data)

print("[%s] saved split data to \"%s\"" % (LOG_SOURCE, data_path))