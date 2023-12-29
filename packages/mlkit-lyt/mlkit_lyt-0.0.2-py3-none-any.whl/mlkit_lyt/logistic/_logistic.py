from math import exp
from numpy import mat, shape, ones


def sigmoid(inX):
    return 1.0 / (1 + exp(-inX))


def gradAscent(dataMatIn, labels, 
               alpha = 0.01, maxCycles = 20):
  """
  count the best weights.
  """

  dataMatrix =  mat(dataMatIn)
  labelMatrix = mat(labels).transpose()

  m,n = shape(dataMatrix)

  weights = ones((n, 1))

  for k in range(maxCycles):

    h = sigmoid(sum(dataMatrix * weights))

    error = (labelMatrix - h )
    weights = weights + alpha * dataMatrix.transpose() * error

  return weights


def classify(inX, weights):
  prob = sigmoid(inX * weights)
  return 1 if prob > 0.5 else 0

