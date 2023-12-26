'''
© Copyright ArdillaByte Inc. 2023
-----------------------------------------------
NN arquitectures
-----------------------------------------------
'''
import torch
from typing import List, Union
from copy import deepcopy



class MLP(torch.nn.Module):
    '''
    A Multi-layer Perceptron
    '''
    def __init__(self, 
                 sizes:List[int], 
                 intermediate_activation_function:any,
                 last_activation_function:Union[None, any]):
        """
        Args:
            sizes (list): list with the sizes of the layers. 
                          The convention is sizes[0] is the size of the input layer
                          and sizes[-1] is the size of the output layer.
            last_activation_function (an activation function)
        """
        super().__init__()
        assert(len(sizes) > 1)
        self.sizes = sizes
        self.intermediate_activation_function = intermediate_activation_function
        self.last_activation_function = last_activation_function
        # -------------------------------------
        # Defining the layers
        # -------------------------------------
        self.model = torch.nn.Sequential()
        # # Apply batch normalization to input
        # self.model.append(torch.nn.BatchNorm1d(sizes[0]))
        for i in range(len(sizes) - 1):
            n_from = sizes[i]
            n_to = sizes[i+1]
            # print(f'Creando capa lineal {n_from} x {n_to}')
            self.model.append(torch.nn.Linear(n_from, n_to))
            # if i < len(sizes) - 3:
            #     # print('Incluyendo layer norm')
            #     self.model.append(torch.nn.LayerNorm(n_to))
            if i < len(sizes) - 2:
                # print('Incluyendo activación')
                self.model.append(self.intermediate_activation_function)
        if self.last_activation_function is not None:
            self.model.append(self.last_activation_function)

    def forward(self, x_in):
        """The forward pass of the network        
        Args:
            x_in (torch.Tensor): an input data tensor. 
        Returns:
            the resulting tensor.
        """
        # Run the input through layers 
        # if len(x_in.shape) == 1:
        #     x_in = x_in.unsqueeze(dim=0)
        return self.model(x_in)
    