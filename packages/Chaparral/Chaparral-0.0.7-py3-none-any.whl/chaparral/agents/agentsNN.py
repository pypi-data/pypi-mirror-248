'''
© Copyright ArdillaByte Inc. 2023
-----------------------------------------------
Classes for implementing the learning methods for 
large and for continuum state spaces using Neural Networks
as approximation function for Q values.
We assume a discrete action space.
We assume epsilon-greedy action selection.
-----------------------------------------------
'''
from . BaseAgent import AgentNN
from copy import deepcopy
import torch
from torch.utils.data import Dataset, DataLoader
from typing import Dict, List, Tuple
import numpy as np
from pathlib import Path


class ExperienceDataset(Dataset):
    '''s
    Creates the dataset out of the experience stream
    '''
    def __init__(
            	self, 
                states:List[torch.Tensor], 
                actions:List[int], 
                updates:List[float]
            ) -> None:
        self.states = states
        self.actions = actions
        self.updates = [torch.tensor(u, dtype=torch.float32) for u in updates]
        n = len(self.states)
        assert (len(self.actions) == n)
        assert (len(self.updates) == n)

    def __len__(self):
        return len(self.states)

    def __getitem__(self, idx:int):
        # print(type(self.states[idx]))
        # print(type(self.actions[idx]))
        # print(type(self.updates[idx]))
        state = self.states[idx].to(torch.float32)
        action = int(self.actions[idx])
        update = self.updates[idx].to(torch.float32) 
        return state, action, update



class DQN(AgentNN) :
    '''
    Implements the Deep Q Network with 
    experience replay and target network.
    '''
    def __init__(self, parameters:Dict[str, any]) -> None:
        super().__init__(parameters)
        self.target_network_latency = parameters["target_network_latency"]
        self.len_exp = parameters["len_exp"]
        self.batch_size = parameters["batch_size"]
        self.num_epochs = parameters["num_epochs"]
        # Create target network
        self.NN_hat = deepcopy(self.NN)
        self.learn_debug = False

    def update(
            	self, 
                next_state:torch.Tensor, 
                reward:float, 
                done:bool
            ) -> None:
        '''
        Agent updates NN with experience replay and updates target NN.
        '''
        n = len(self.actions)
        k = self.len_exp
        # Obtain length of experience
        if n < k:
            # print('agent only learns with enough experience')
            #agent only learns with enough experience
            pass
        else:
            # Create the experience stream with random indices from the whole history
            states, actions, next_states, rewards, dones = self.create_experience_stream(next_state, reward, done)
            # Create the dataset and dataloader
            ds = self.create_dataset(states, actions, next_states, rewards, dones)
            # Train for number of epochs
            # print('Training...')
            for e in range(self.num_epochs):
                ds_loader = DataLoader(ds, batch_size=self.batch_size, shuffle=True)
                self.NN.learn(ds_loader)
            # Check if it's turn to update the target network
            # if len(self.actions) % self.target_network_latency == 0 or done:
            if len(self.actions) % self.target_network_latency == 0:
                # print('Updating Target Network')
                self.NN_hat = deepcopy(self.NN)

    def create_experience_stream(
            	self, 
                next_state:any, 
                reward:float, 
                done:bool
            ) -> Tuple[
					List[any], 
					List[int], 
					List[any], 
					List[float], 
					List[bool]
	            ]:
        # Get records
        states = list(self.states)[:-1].copy()
        actions = list(self.actions)[:-1].copy()
        next_states = list(self.states)[1:].copy()
        rewards = list(self.rewards)[1:].copy()
        dones = list(self.dones)[1:].copy()
        # Check lists are in good shape
        lengths = f'#states:{len(self.states)} -- #actions:{len(self.actions)} -- #rewards:{len(self.rewards)} -- #dones:{len(self.dones)}'
        n = len(self.states)
        assert(n > 1), 'Error: len_experience should be at least 2'
        assert(len(self.actions) == n), lengths
        assert(len(self.rewards) == n), lengths
        assert(len(self.dones) == n), lengths
        # Create mask with random indices
        mask = np.random.choice(range(len(self.states) - 1), 
                                size=self.len_exp - 1, 
                                replace=False)
        tensor_mask = torch.tensor(mask).to(torch.int32)
        # print('mask:', tensor_mask, type(tensor_mask))
        # Get the randomly selected states
        stacked_states = torch.stack([state for state in self.states])
        filtered_states = torch.index_select(stacked_states, 0, tensor_mask)
        list_of_states = list(torch.unbind(filtered_states, dim=0))
        states = list_of_states + [self.states[-1]]
        # Get the randomly selected NEXT states
        mask_next = (np.array(mask) + 1).tolist()
        tensor_mask = torch.tensor(mask_next)
        next_states = list_of_states + [next_state]
        # Get the randomly selected actions
        actions = np.array(self.actions.copy())[mask].tolist() + [self.actions[-1]]
        # Get the randomly selected rewards
        rewards = np.array(self.rewards.copy())[mask_next].tolist() + [reward]
        # Get the randomly selected dones
        dones = np.array(self.dones.copy())[mask_next].tolist() + [done]
        # Make sure indices don't correspond to terminal satates
        states, actions, next_states, rewards, dones = self.avoid_indices_for_terminal_states(states, actions, next_states, rewards, dones)
        # Check lists are in good shape
        self._check_lists_in_good_shape(states, actions, next_states, rewards, dones)
        return states, actions, next_states, rewards, dones

    def avoid_indices_for_terminal_states(
            	self,
                states:List[torch.Tensor], 
                actions:List[int], 
                next_states:List[torch.Tensor], 
                rewards:List[float], 
                dones:List[bool]
            ) -> Tuple[
                	List[any], 
                    List[int], 
                    List[any],
                    List[float], 
                    List[bool]
                ]:
        indices_no_terminal_states = [i for i, a in enumerate(actions) if not np.isnan(a)]
        # Filtering lists
        actions = np.array(actions.copy())[indices_no_terminal_states].tolist()
        rewards = np.array(rewards.copy())[indices_no_terminal_states].tolist()
        dones = np.array(dones.copy())[indices_no_terminal_states].tolist()
        # Filtering lists of tensors
        tensor_mask = torch.tensor(indices_no_terminal_states)
        #     list of states
        stacked_states = torch.stack(states)
        filtered_states = torch.index_select(stacked_states, 0, tensor_mask)
        states = list(torch.unbind(filtered_states, dim=0))
        #     list of next_states
        stacked_states = torch.stack(next_states)
        filtered_states = torch.index_select(stacked_states, 0, tensor_mask)
        next_states = list(torch.unbind(filtered_states, dim=0))
        return states, actions, next_states, rewards, dones

    def create_dataset(self, 
                states:List[torch.Tensor], 
                actions:List[int], 
                next_states:List[torch.Tensor], 
                rewards:List[float], 
                dones:List[bool]
            ) -> ExperienceDataset:
        updates = [self.get_update(next_states[i], rewards[i], dones[i]) for i in range(len(rewards))]
        states, actions, updates = self.filter_ds(states, actions, updates)
        n = len(states)
        assert(n > 0)
        return ExperienceDataset(states, actions, updates)
               
    def filter_ds(self, states, actions, updates):
        mask = [i for i, state in enumerate(states) if state[0] != 0]
        tensor_mask = torch.tensor(mask).to(torch.int32)
        stacked_states = torch.stack([state for state in states])
        filtered_states = torch.index_select(stacked_states, 0, tensor_mask)
        list_of_states = list(torch.unbind(filtered_states, dim=0))
        return list_of_states, np.array(actions)[mask].tolist(), np.array(updates)[mask].tolist()

    def get_update(
                self, 
                next_state:torch.Tensor, 
                reward:float, 
                done:bool
            ) -> float:
        if done:
            # Episode is finished. No need to bootstrap update
            G = reward
            if self.learn_debug:
                print(f'G:{G} --- reward:{reward} --- ENV DONE')
        else:
            # Episode is active. Bootstrap update using Target Network
            Qvals = self.NN_hat.values_vector(next_state)
            maxQ = max(Qvals)
            G = reward + self.gamma * maxQ
            if self.learn_debug:
                print(f'G:{G} --- reward:{reward} --- gamma:{self.gamma} --- maxQ:{maxQ}')
        return G    
    
    def restart(self) -> None:
        # Override restart to preserve experience
        if len(self.rewards) > 1:
            # print('Including empty rewards and dones at begining of episode')
            self.rewards.append(np.nan)
            self.dones.append(np.nan)
        self.NN.restart()

    def get_records(self) -> Tuple[
									List[any],
									List[int],
									List[any],
									List[float],
									List[bool]
                                ]:
        # Get records
        states = list(self.states)[:-1].copy()
        actions = list(self.actions)[:-1].copy()
        next_states = list(self.states)[1:].copy()
        rewards = list(self.rewards)[1:].copy()
        dones = list(self.dones)[1:].copy()
        self._check_lists_in_good_shape(states, actions, next_states, rewards, dones)
        # Make sure indices don't correspond to terminal satates
        states, actions, next_states, rewards, dones = self.avoid_indices_for_terminal_states(states, actions, next_states, rewards, dones)
        self._check_lists_in_good_shape(states, actions, next_states, rewards, dones)
        return states, actions, next_states, rewards, dones

    def print_dataset(self) -> None:
        # Download records
        states, actions, next_states, rewards, dones = self.get_records()
        # Create the dataset
        ds = self.create_dataset(states, actions, next_states, rewards, dones)
        # Create the dataloader
        ds_loader = DataLoader(ds, batch_size=1, shuffle=False)
        for state, action, update in ds_loader:
            print('')
            print('='*30)
            print('state:')
            print(state)
            print('-'*20)
            print(f'Action:\n\t{action}')
            print('-'*20)
            print(f'Update:\n\t{update}')

    def _check_lists_in_good_shape(
                self,
                states:List[any],
                actions:List[int],
                next_states:List[any],
                rewards:List[float],
                dones:List[bool]
            ) -> None:
        # Check lists are in good shape
        lengths = f'#states:{len(states)} -- #actions:{len(actions)} #next_states:{len(next_states)} -- #rewards:{len(rewards)} -- #dones:{len(dones)}'
        n = len(states)
        assert(len(next_states) == n), lengths
        assert(len(actions) == n), lengths
        assert(len(rewards) == n), lengths
        assert(len(dones) == n), lengths



