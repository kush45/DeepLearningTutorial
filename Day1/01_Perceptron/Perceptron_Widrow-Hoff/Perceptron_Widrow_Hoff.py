import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

#     ADAptive LInear NEuron (ADALINE) by Bernard Widrow and Tedd Hoff
#     Illustrates the key concept of defining and minimizing cost functions,
#     which will lay the ground work for understanding more advanced machine learning algorithms for classification,
#     such as logistic regression and support vector machines, etc.

#     Key difference between Widrow-Hoff rule and Rosenblatt's Perceptron is that
#     the weights are updated based on a linear activation function rather than a unit step function
#     i.e., [1 x] * weights - sum - linear activation - (compute errors) - quantizer - output

#     Compared to Rosenblatt's Perceptron, in ADALINE, the weight update is calculated based on all samples
#     in the training set (instead of updating the weights incrementally after each sample),
#     which is why this approach is also referred to as "batch" gradient descent.
class AdalineGD(object):
    """
    Parameters: eta, epochs
    Attributes: weights, errors
    """

    def __init__(self, eta=0.01, epochs=10):
        self.eta = eta
        self.epochs = epochs

    def train(self, X, y):
        """
        X: {array-like}, shape=[num_samples, num_features]
        y: {array-like}, shape=[num_samples]
        """
        self.weights = np.zeros(1 + X.shape[1])  # 1 for bias
        self.cost = []

        for i in range(self.epochs):
            output = self.net_input(X)
            errors = (y - output)
            self.weights[1:] += self.eta * X.T.dot(errors)
            self.weights[0] += self.eta * errors.sum()
            cost = (errors ** 2).sum() / 2.0
            self.cost.append(cost)
        return self

    def net_input(self, X):
        return np.dot(X, self.weights[1:]) + self.weights[0]

    def activation(self, X):
        return self.net_input(X)

    def predict(self, X):
        return np.where(self.activation(X) >= 0.0, 1, -1)


def plot_decision_regions(X, y, classifier, resolution=0.02):
    # setup marker generator and color map
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1

    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    # plot class samples
    for idx, c1 in enumerate(np.unique(y)):
        plt.scatter(x=X[y == c1, 0], y=X[y == c1, 1], alpha=0.8, c=cmap(idx), marker=markers[idx], label=c1)