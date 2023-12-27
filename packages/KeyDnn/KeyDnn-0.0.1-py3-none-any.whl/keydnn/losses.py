from keydnn.utilities import ComplexFunction

from typing import *

import numpy as np 

class Loss(ComplexFunction):

    def __init__(self, function   : Optional[ Callable ] = None,
                       derivative : Optional[ Callable ] = None,
                       inference  : Optional[ Callable ] = None) -> None:

        super(Loss, self).__init__(function, derivative, inference)

SumSquaredError = SSE = Loss()

@SSE.define_function
def _sse_function(self, y_true : np.ndarray, y_pred : np.ndarray) -> np.ndarray:

    if (self.DEBUG_MODE):

        assert isinstance(y_true, np.ndarray)

        assert isinstance(y_pred, np.ndarray)

    return np.square(y_pred - y_true)

@SSE.define_derivative
def _sse_derivative(self, y_true : np.ndarray, y_pred : np.ndarray) -> np.ndarray:

    if (self.DEBUG_MODE):

        assert isinstance(y_true, np.ndarray)

        assert isinstance(y_pred, np.ndarray)

    return 2.0 * (y_pred - y_true)

@SSE.define_inference
def _sse_inference(self, y_true : np.ndarray, y_pred : np.ndarray) -> np.ndarray:

    if (self.DEBUG_MODE):

        assert isinstance(y_true, np.ndarray)

        assert isinstance(y_pred, np.ndarray)

    return np.sum(self.call_function(y_true, y_pred))

if (__name__ == "__main__"):

    y_true = np.array([ 1, 2, 3, 5, 6 ])

    y_pred = np.array([ 3, 3, 3, 3, 3 ])

    output = SSE.call_function(y_true, y_pred)

    print(output)

    output = SSE.call_derivative(y_true, y_pred)

    print(output)

    output = SSE.call_inference(y_true, y_pred)

    print(output)

    output = SSE(y_true, y_pred)

    print(output)