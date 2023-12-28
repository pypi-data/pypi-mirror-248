'''
© Copyright ArdillaByte Inc. 2023
-----------------------------------------------
Implements:
    - the base tabular agent, Agent
    - the base agent for Q approximation, AgentCS
    - the base agent for Q approximations based on Neural Networks, AgentNN
    - the base agent for policy learning, PolicyAgent
-----------------------------------------------
'''

import numpy as np
from typing import Dict
import json
from copy import deepcopy
from typing import Optional
from pathlib import Path
from termcolor import colored
from collections import deque


class AgentNN() :
    '''
    Super class of agents with Q approximation
    using Neural Networks.
    '''

    def __init__(self, parameters:dict):
        self.parameters = parameters
        self.nA = self.parameters['nA']
        self.gamma = self.parameters['gamma']
        self.epsilon = self.parameters['epsilon']
        self.NN = self.parameters['NN']
        assert(hasattr(self.NN, 'predict')), 'NN must be an object with a predict() method'
        assert(hasattr(self.NN, 'values_vector')), 'NN must be an object with a values_vector() method'
        assert(hasattr(self.NN, 'learn')), 'NN must be an object with a learn() method'
        assert(hasattr(self.NN, 'save')), 'NN must be an object with a save() method'
        assert(hasattr(self.NN, 'load')), 'NN must be an object with a load() method'
        assert(hasattr(self.NN, 'reset')), 'NN must be an object with a reset() method'
        self.max_len = self.parameters['max_len']
        self.states = deque(maxlen=self.max_len)
        self.actions = deque(maxlen=self.max_len)
        self.rewards = deque([np.nan], maxlen=self.max_len)
        self.dones = deque([np.nan], maxlen=self.max_len)
        self.seed = None
        self.debug = False
        # Create model file
        self.model_folder = Path.cwd() / Path('..').resolve() / Path('..').resolve() / Path('models', 'MLP')
        # self.model_folder.mkdir(parents=True, exist_ok=True)
        self.model_file = self.model_folder / Path('mlp.pt')

    def make_decision(self, state:Optional[any]=None):
        '''
        Agent makes an epsilon greedy accion based on Q values.
        '''
        if np.random.uniform(0,1) < self.epsilon:
            return np.random.choice(range(self.nA))
        else:
            if state is None:
                state = self.states[-1]
            return self.argmaxQ(state)        

    def argmaxQ(self, state):
        '''
        Determines the action with max Q value in state s
        '''
        Qvals = self.NN.values_vector(state)
        maxQ = max(Qvals)
        opt_acts = [a for a, q in enumerate(Qvals) if np.isclose(q, maxQ)]
        if self.seed is not None:
            np.random.seed(self.seed)
        try:
            argmax = np.random.choice(opt_acts)
            return argmax
        except Exception as e:
            print('')
            print(colored('%'*50, 'red'))
            print(colored(f'Error in argmaxQ ====>', 'red'))
            print(colored(f'state:\n\t{state}', 'red'))
            print('')
            print(colored(f'Qvals:{Qvals}', 'red'))
            print(colored(f'len:{len(Qvals)} --- type:{type(Qvals)}', 'red'))
            print('')
            print(colored(f'maxQ:{maxQ}', 'red'))
            print(colored(f'type:{type(maxQ)}', 'red'))
            print('')
            print(colored(f'opt_acts:{opt_acts}', 'red'))
            print(colored(f'opt_acts:{[a for a, q in enumerate(Qvals) if np.isclose(q, maxQ)]}', 'red'))
            print(colored('%'*50, 'red'))
            print('')
            raise Exception(e)            

    def update(self, next_state, reward, done) -> None:
        '''
        Agent updates its NN according to a model.
            TO BE OVERWRITTEN BY SUBCLASS  
        '''
        pass

    def restart(self) -> None:
        '''
        Restarts the agent for a new trial.
        '''
        self.states = deque(maxlen=self.max_len)
        self.actions = deque(maxlen=self.max_len)
        self.rewards = deque([np.nan], maxlen=self.max_len)
        self.dones = deque([np.nan], maxlen=self.max_len)
        self.NN.restart()

    def reset(self) -> None:
        '''
        Resets the agent for a new simulation.
        '''
        self.restart()
        # Resets the NN
        self.NN.reset()
    
    def save(self, file:Path) -> None:
        self.NN.save(file=file)

    def load(self, file:Path) -> None:
        self.NN.load(file=file)
