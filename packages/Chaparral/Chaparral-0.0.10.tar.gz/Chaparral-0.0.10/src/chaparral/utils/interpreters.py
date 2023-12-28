'''
© Copyright ArdillaByte Inc. 2023

------------------------------------
Module with the state interpreters.
------------------------------------
'''
import numpy as np
import torch
from typing import Union, Tuple

def id_state(state):
    '''
    Default interpreter: do nothing.
    '''
    return state

def gym_interpreter1(state):
    '''
    Cleans the state and get only the state space.
    When states come from gymnasium, they contain 
    additional info besides the state space.
    '''
    if isinstance(state, tuple):
        if isinstance(state[1], dict):
            state = state[0]
        else:
            state = state
    else:
        state = state
    return state

def gym_interpreter2(state):
    '''
    Cleans the state and get only the state space.
    When states come from gymnasium, they contain 
    additional info besides the state space.
    Returns a pytorch tensor.
    '''
    if isinstance(state, tuple):
        if isinstance(state[1], dict):
            state = state[0]
        else:
            state = state
    else:
        state = state
    return torch.tensor(state, dtype=torch.float32)

def triqui_interpreter(state):
    '''
    Interprets triqui state as a ravel index.
    '''
    shape = tuple([3]*9)
    comps = tuple(state.flatten().tolist()[0])
    indice = np.ravel_multi_index(comps, shape)
    return indice

def blackjack_interpreter(state):
    '''
    Interprets blackjack state as a ravel index.
    The observation consists of a 3-tuple containing: 
        the player’s current sum, 
        the value of the dealer’s one showing card (1-10 where 1 is ace), 
        and whether the player holds a usable ace (0 or 1).
    The observation is returned as (int(), int(), int()).
    We transform the 3-tuple into an index using numpy.ravel_multi_index
    '''
    shape = (32, 11, 2)
    # Ignore extra info from state
    if len(state) == 2:
        state_ = state[0] 
    else:
        state_ = state
    indice = np.ravel_multi_index(state_, shape)
    return indice

def PitL_nS_interpreter(state):
    '''
    Interprets PitLaberynth state as a ravel index.
    '''
    shape = (state.shape[1], state.shape[2])
    comps = np.where(state == 1)
    to_ravel = [(comps[1][i],comps[2][i]) for i in range(len(comps[0]))]
    ravels = [np.ravel_multi_index(mi, shape) for mi in to_ravel]
    n = np.product(shape)
    n_shape = (n, n, n, n)
    return np.ravel_multi_index(ravels, n_shape)

def PitL_cs_interpreter(state):
    '''
    Interprets PitLaberynth state as a triple.
    '''
    shape = (state.shape[1], state.shape[2])
    comps = np.where(state == 1)
    to_ravel = [(comps[1][i],comps[2][i]) for i in range(len(comps[0]))]
    ravels = [np.ravel_multi_index(mi, shape) for mi in to_ravel]
    return tuple(ravels)

def PitL_vector_interpreter(state):
    '''
    Interprets PitLaberynth state as a single vector
    '''
    shape = np.product(state.shape)
    return state.reshape(1, shape)

def PitL_CNN_interpreter(state:np.ndarray) -> torch.tensor:
    '''
    Interprets PitLaberynth state as an image
    with 4 channels and returns a pytorch tensor
    with only 1 channel
    '''
    projection = np.zeros(state[0].shape)
    # Projecting layers
    for i, layer in enumerate(state):
        projection += layer*(i+1)
    # Converting to tensor
    projection = torch.tensor(projection, dtype=torch.float32)
    # Unsqeeze for convolutional network with 1 channel
    projection = projection.unsqueeze(dim=0)
    return projection

def GridW_CNN_interpreter(state:Union[int, Tuple]) -> torch.tensor:
    '''
    Interprets GridWorld state as an image
    with 1 channel and returns a pytorch tensor
    '''
    # Initialize array
    state_ = np.zeros((4,4))
    if isinstance(state, int) or isinstance(state, np.int64):
        # Find coordinates
        Y, X = np.unravel_index(state, (4,4))
    elif isinstance(state, Tuple):
        X, Y = state
        X, Y = int(X), 3 - int(Y)
    else:
        raise Exception(f'Unreadable state {state}. Must be of type int or tuple, got {type(state)}')
    # See as matrix indices
    row = 3 - Y
    col = X
    state_[row,col] = 1
    # Convert to tensor
    state_ = torch.tensor(state_, 
                          dtype=torch.float32)
    # Unsqeeze for convolutional network with 1 channel
    state_ = state_.unsqueeze(dim=0)
    return state_
