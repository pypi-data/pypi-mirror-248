from typing import *

import numpy as np

from keydnn.utilities import ComplexFunction

class Activation(ComplexFunction):

    ACTIVATION_FUNCTIONS = {}

    ACTIVATION_COUNTER = 1

    @classmethod
    def _add_activation_instance(cls, name : str, target_instance : "Activation") -> None:

        if (cls.DEBUG_MODE):
            assert isinstance(target_instance, Activation)

        if (name == ""):
            raise ValueError("Activation layer name cannot be empty")

        if (name in cls.ACTIVATION_FUNCTIONS):
            raise KeyError(f"Activation layer name collision. The following name already exists: `{name}`")

        cls.ACTIVATION_FUNCTIONS[name] = target_instance

    @classmethod
    def __generate_instance_name(cls) -> str:

        instance_name = f"unknown_activation_function_{cls.ACTIVATION_COUNTER}"

        cls.ACTIVATION_COUNTER += 1

        return instance_name

    def __init__(self, function   : Optional[ Callable ] = None,
                       derivative : Optional[ Callable ] = None,
                       inference  : Optional[ Callable ] = None, *,
                       name       : Optional[ str ]      = None) -> None:

        if (self.DEBUG_MODE):
            assert ((name is None) or (isinstance(name, str)))

        self.name = ((self.__generate_instance_name()) if (name is None) else (name))

        super(Activation, self).__init__(function, derivative, inference)

        self._add_activation_instance(self.name, self)

Sigmoid = sigmoid = Activation(name = "sigmoid")

@Sigmoid.define_function
def _sigmoid_function(self, x : np.ndarray) -> np.ndarray:

    if (self.DEBUG_MODE):
        assert isinstance(x, np.ndarray)

    return 1.0 / (1.0 + np.exp(-x))

@Sigmoid.define_derivative
def _sigmoid_derivative(self, x : np.ndarray) -> np.ndarray:

    if (self.DEBUG_MODE):
        assert isinstance(x, np.ndarray)

    value = self.call_function(x)

    return value * (1 - value)

@Sigmoid.define_inference
def _sigmoid_inference(self, x : np.ndarray) -> np.ndarray:

    if (self.DEBUG_MODE):
        assert isinstance(x, np.ndarray)

    return self.call_function(x)

ReLU = relu = Activation(name = "relu")

@ReLU.define_function
def _relu_function(self, x : np.ndarray) -> np.ndarray:

    if (self.DEBUG_MODE):
        assert isinstance(x, np.ndarray)

    return np.maximum(0, x)

@ReLU.define_derivative
def _relu_derivative(self, x : np.ndarray) -> np.ndarray:

    if (self.DEBUG_MODE):
        assert isinstance(x, np.ndarray)

    return np.float32(x > 0)

@ReLU.define_inference
def _relu_inference(self, x : np.ndarray) -> np.ndarray:

    if (self.DEBUG_MODE):
        assert isinstance(x, np.ndarray)

    return self.call_function(x)

TanH = tanh = Activation(name = "tanh")

@TanH.define_function
def _tanh_function(self, x : np.ndarray) -> np.ndarray:

    if (self.DEBUG_MODE):
        assert isinstance(x, np.ndarray)

    return ((2.0) / (1 + np.exp(-2 * x)) - 1.0)

@TanH.define_derivative
def _tanh_derivative(self, x : np.ndarray) -> np.ndarray:

    if (self.DEBUG_MODE):
        assert isinstance(x, np.ndarray)

    return (1 - np.power(self.call_function(x), 2))

@TanH.define_inference
def _tanh_inference(self, x : np.ndarray) -> np.ndarray:

    if (self.DEBUG_MODE):
        assert isinstance(x, np.ndarray)

    return self.call_function(x)

if (__name__ == "__main__"):

    print(Activation.ACTIVATION_FUNCTIONS)

    test_classes = [ TanH, Sigmoid, ReLU, sigmoid, relu, tanh ]

    for test_class in test_classes:

        test_data = np.array([ 1, 2, 3, 4, -5 ])

        test_output = test_class.call_function(test_data)

        print(test_output.shape)

        print(test_output)

        test_output = test_class.call_derivative(test_data)

        print(test_output.shape)

        print(test_output)

        test_output = test_class.call_inference(test_data)

        print(test_output.shape)

        print(test_output)

        test_output = test_class(test_data)

        print(test_output.shape)

        print(test_output)