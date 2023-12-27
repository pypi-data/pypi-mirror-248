from typing import *

from keydnn.utilities import bytes2string, string2bytes

from keydnn.utilities import NetworkLayer, NeuralNetwork

from keydnn.activations import Activation

import numpy as np 

@NeuralNetwork.register_layer
class Linear(NetworkLayer):

    @classmethod
    def export_to_dict(cls, layer : "Linear") -> Dict[ str, Union[ str, int, bytes ] ]:

        if (cls.DEBUG_MODE):
            assert isinstance(layer, Linear)

        output_data = {
            "weights" : {
                "W" : bytes2string(layer._W.tobytes()),
                "B" : bytes2string(layer._B.tobytes())
            },
            "shape" : {
                "I" : layer._input_size,
                "O" : layer._output_size
            },
            "dtype" : {
                "W" : layer._W.dtype.str,
                "B" : layer._B.dtype.str
            },
            "activation" : {
                "A" : (("") if (layer._activation is None) else (layer._activation.name))
            }
        }

        return output_data

    @classmethod
    def import_from_dict(cls, layer_data : Dict[ str, Union[ str, int, bytes ] ]) -> "Linear":

        if (cls.DEBUG_MODE):
            assert isinstance(layer_data, dict)

        linear_layer = Linear(
            input_size  = layer_data["shape"]["I"],
            output_size = layer_data["shape"]["O"],
            activation  = Activation.get_activation_layer(layer_data["activation"]["A"], None)
        )

        linear_layer._W = np.reshape(
            np.frombuffer(string2bytes(layer_data["weights"]["W"]), dtype = layer_data["dtype"]["W"]),
            (layer_data["shape"]["O"], layer_data["shape"]["I"])
        )

        linear_layer._B = np.reshape(
            np.frombuffer(string2bytes(layer_data["weights"]["B"]), dtype = layer_data["dtype"]["B"]),
            (layer_data["shape"]["O"], 1)
        )

        return linear_layer

    def __init__(self, input_size  : int,
                       output_size : int,
                       activation  : Optional[ Union[ Activation, str ] ] = None) -> None:

        if (self.DEBUG_MODE):

            assert isinstance(input_size, int)

            assert isinstance(output_size, int)

            assert ((activation is None) or (isinstance(activation, Activation)) or (isinstance(activation, str)))

            assert input_size > 0

            assert output_size > 0

        # basic parameters

        self._input_size  = input_size

        self._output_size = output_size

        self._activation  = activation

        if (isinstance(self._activation, str)):

            if not (Activation.contains_activation_layer(self._activation)):
                raise KeyError(f"The name of the following activation layer could not be found: `{self._activation}`")
            
            self._activation = Activation.get_activation_layer(self._activation)

        # layer weights and biases

        self._W = np.random.uniform(-0.5, 0.5, size = (self._output_size, self._input_size))

        self._B = np.random.uniform(-0.5, 0.5, size = (self._output_size, 1))

        # optimizer parameters : temporary values and gradients

        self._W_gradients = np.zeros_like(self._W)

        self._B_gradients = np.zeros_like(self._B)

        self._track_grads = True

        self._X = None

        self._Z = None

        self._A = None

    def clear_gradients(self) -> None:

        self._W_gradients.fill(0)

        self._B_gradients.fill(0)

    def optimize(self, learning_rate   : Optional[ Union[ float, int ] ] = 0.001, *,
                       clear_gradients : Optional[ bool ] = False) -> None:

        if (self.DEBUG_MODE):

            assert ((isinstance(learning_rate, float)) or (isinstance(learning_rate, int)))

            assert learning_rate > 0

        if (self._track_grads == False):
            raise Warning("Optimizing model weights without tracking gradients. Consider enabling gradients by calling `use_gradients`.")

        # update weights and biases

        self._W -= (learning_rate * self._W_gradients)

        self._B -= (learning_rate * self._B_gradients)

        # clear gradients if specified by engineer

        if (clear_gradients):
            self.clear_gradients()

    def get_weights(self) -> Tuple[ np.ndarray, np.ndarray ]:

        return (self._W.copy(), self._B.copy())

    def without_gradients(self) -> None:

        # should not track gradients
        self._track_grads = False

    def use_gradients(self) -> None:

        # should track gradients
        self._track_grads = True

    def forward(self, x : np.ndarray) -> np.ndarray:

        if (self.DEBUG_MODE):
            assert isinstance(x, np.ndarray)

        # (B, O) <= (O, I) x (B, I) + (B, O)
        Z = np.einsum("OI,BI->BO", self._W, x, optimize = True) + self._B.T

        # (B, O)
        A = Z

        if (self._activation is not None):

            # (B, O)
            A = self._activation.call_function(Z)

        # should track temporary values for back propagation

        if (self._track_grads):

            # (B, I)
            self._X = x.copy()

            # (B, O)
            self._Z = Z

            # (B, O)
            self._A = A

        else:

            self._X = None

            self._Z = None

            self._A = None

        return A

    def backward(self, gradient : np.ndarray) -> np.ndarray:

        # gradient : (B, O)

        if (self.DEBUG_MODE):
            assert isinstance(gradient, np.ndarray)

        if (self._track_grads == False):
            raise ValueError("Back propagation without gradients is forbidden. Try enabling gradients by calling `use_gradients`.")

        if (any((x is None) for x in [ self._X, self._Z, self._Z ])):
            raise ValueError("Back propagation before forward propagation is forbidden. Try calling `forward` first.")

        # (B, O) : initialize ones-matrix if activation is undefined
        dA_dZ = np.ones_like(gradient)

        if (self._activation is not None):

            # (B, O) : partial derivative of activation with respect to Z
            dA_dZ = self._activation.call_derivative(self._Z)

        # Z Formula : [ Z = WX + B : (O, 1) = (O, I) x (I, 1) ]

        # (O, 1) : initialized with ones
        dZ_dB = np.ones_like(self._B)

        # (B, O) <= (B, O) * (B, O)
        dZ = gradient * dA_dZ

        # (O, 1) <= (O,) <= (B, O) <= (B, O) x (1, O)
        dB = np.reshape(np.sum(dZ * dZ_dB.T, axis = 0), (self._output_size, 1))

        # (O, I) <= (B, O, I) <= (B, O) x (B, I)
        dW = np.sum(np.einsum("BO,BI->BOI", dZ, self._X, optimize = True), axis = 0)

        # (B, I) <= (O, I) x (B, O)
        dX = np.einsum("OI,BO->BI", self._W, dZ, optimize = True)

        # (O, 1) <= (O, 1) + (O, 1)
        self._B_gradients += dB

        # (O, I) <= (O, I) + (O, I)
        self._W_gradients += dW

        return dX

if (__name__ == "__main__"):

    from activations import ReLU, Sigmoid

    from losses import SSE

    test_input = np.array([
        [ 0, 0 ], [ 0, 1 ], [ 1, 0 ], [ 1, 1 ]
    ])

    test_label = np.array([
        [ 1, 0 ], [ 0, 1 ], [ 0, 1 ], [ 1, 0 ]
    ])

    layer_1 = Linear(input_size = 2, output_size = 32, activation = "tanh")

    layer_2 = Linear(input_size = 32, output_size = 2, activation = "softmax")

    layer_1.without_gradients()

    layer_2.without_gradients()

    for epoch in range(2000):

        layer_1.use_gradients()

        layer_2.use_gradients()

        y_pred = layer_1.forward(test_input)

        y_pred = layer_2.forward(y_pred)

        loss_gradient = SSE.call_derivative(test_label, y_pred)

        loss_gradient = layer_2.backward(loss_gradient)

        loss_gradient = layer_1.backward(loss_gradient)

        layer_2.optimize(learning_rate = 0.1)

        layer_1.optimize(learning_rate = 0.1)

        if (epoch % 200 == 0):
            print(f"Epoch: {epoch + 1}, Loss: {SSE(test_label, y_pred)}")

    layer_1 = Linear.import_from_dict(Linear.export_to_dict(layer_1))

    layer_2 = Linear.import_from_dict(Linear.export_to_dict(layer_2))

    layer_1.without_gradients()

    layer_2.without_gradients()

    layer_output = layer_1.forward(test_input)

    layer_output = layer_2.forward(layer_output)

    print(np.argmax(layer_output, axis = 1))

    print(Linear.export_to_dict(layer_1))