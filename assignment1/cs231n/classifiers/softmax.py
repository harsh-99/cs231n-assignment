import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]
  num_classes = W.shape[1]
  loss = 0.0
  i=1
  for i in xrange(num_train):
    # Compute vector of scores
    f_i = X[i].dot(W)

    # Normalization trick to avoid numerical instability, per http://cs231n.github.io/linear-classify/#softmax
    f_i -= np.max(f_i)

    # Compute loss (and add to it, divided later)
    sum_j = np.sum(np.exp(f_i))
    p = lambda k: np.exp(f_i[k]) / sum_j
    loss += -np.log(p(y[i]))
#     print p(y[i])

    # Compute gradient
    # Here we are computing the contribution to the inner sum for a given i.
#     print p(1)
    for k in range(num_classes):
      p_k = p(k)
      dW[:, k] += (p_k - (k == y[i])) * X[i]
#       print dW[:,k]

  loss /= num_train
  loss += 0.5 * reg * np.sum(W * W)
  dW /= num_train
  dW += reg*W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_train = X.shape[0]
  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  y_compute = X.dot(W)
  y_compute -= np.max(y_compute, axis = 1,keepdims=True)
  sum_j = np.sum(np.exp(y_compute),axis = 1,keepdims=True)
  p = np.exp(y_compute)/sum_j
  loss = np.sum(-np.log(p[np.arange(num_train), y]))  
  loss /= num_train
  loss += reg*W
  ind = np.zeros_like(p)
#   print ind.shape
  ind[np.arange(num_train), y] = 1
  dW = X.T.dot(p - ind)
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

