import numpy as np
import json

def relu(pre_hidden_units):
    """
    Use:
        Introduce non-linearity to hidden layer in network
    Param: 
        z: numpy array of m by n dimensions, pre-activated units (w.x + b)
    Return: 
        0 if z < 0, or z if z > 0
    """
    return np.maximum(0, pre_hidden_units)

def softmax(hidden_units):
    """
    Use:
        transforms final hidden units to probabilities, such that sum(softmax(h)) == 1
    Param: 
        h: batch of hidden units from last hidden of network
    Returns: 
        class probabilities
    """
    return np.exp(hidden_units) / np.sum(np.exp(hidden_units), axis=1, keepdims=True)

def batch(X, y, batch_size):
  num_batches = int(np.ceil(X.shape[0] / batch_size))

  X_batches = np.array_split(X, num_batches)
  y_batches = np.array_split(y, num_batches)

  return X_batches, y_batches

def forward(X):
    """
    push the data through the network
    """
    # output mapping
    output_map = {0:0, 1:45, 2:90, 3:135, 4:180, 5:225, 6:270, 7:315}
    # read in weight and bias data
    with open(r"C:\Users\Patrick\Desktop\5618 project\data\weightsbiases.txt", "r") as fp:
        wb = json.load(fp)

    # input to hidden
    z1 = np.dot(X, wb['w1']) + wb['b1']
    a1 = relu(z1)

    # hidden to output
    z2 = np.dot(a1, wb['w2']) + wb['b2']
    a2 = softmax(z2)

    y_hats = np.argmax(a2, axis=1)
    output = [output_map[label] for label in y_hats]

    return output


