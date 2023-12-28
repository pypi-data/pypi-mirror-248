'''
© Copyright ArdillaByte Inc. 2023

-----------------------------------------------
Class to run, renderize, train and test agents
over environments.
-----------------------------------------------
'''
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from typing import Dict
from os import path
from pathlib import Path
import sys
import chaparral.modelos.entorno as E
from chaparral.utils.interaction import Episode, Experiment
import chaparral.agents.agentsNN as ApproxNN
from chaparral.utils.plot_utils import Plot

SCRIPT_PATH = Path.cwd() / Path('..').resolve()

OWN_ENV_LIST = ['ABC', 'GridworldEnv', 'PitLaberynth']


class Performer :
    '''
    Class to train and run an agent in an environment.
    '''
    def __init__(self,\
                env_name:str,\
                env_parameters:Dict[str, any],\
                state_interpreter:any,\
                agent_name:str,\
                agent_parameters:Dict[str,any]
                ) -> None:
        #--------------------------------
        # Environment metadata
        #--------------------------------
        self.env_name = env_name
        assert(isinstance(env_parameters, dict))
        self.env_parameters = env_parameters
        # to check if environment is given to use
        self.use_environment = False
        self.state_interpreter = state_interpreter
        #--------------------------------
        # Agent metadata
        #--------------------------------
        if '.' in agent_name:
          agent_class, agent_name = agent_name.split('.')
        else:           
          agent_class = 'TableAgents'
        self.agent_name = agent_name
        self.agent_class = agent_class
        self.agent_parameters = agent_parameters
        if 'deep' in agent_parameters.keys():
          self.deep = agent_parameters['deep']
        else:
          self.deep = False
        self.dict_paths = self.consolidate_folders()
        self.data = None

    def consolidate_folders(self) -> Dict[str,Path]:
        """Create folders to store model files"""
        dict_paths = dict()
        dict_paths['file_name'] = f'{self.agent_name}_in_{self.env_name}'
        dict_paths['image_folder'] = SCRIPT_PATH / Path('images', dict_paths['file_name'])
        # dict_paths['image_folder'].mkdir(parents=True, exist_ok=True)
        dict_paths['data_folder'] = SCRIPT_PATH / Path('data', dict_paths['file_name'])
        # dict_paths['data_folder'].mkdir(parents=True, exist_ok=True)
        dict_paths['model_folder'] = SCRIPT_PATH / Path('models', dict_paths['file_name'])
        # dict_paths['model_folder'].mkdir(parents=True, exist_ok=True)
        dict_paths['video_folder'] = SCRIPT_PATH / Path('videos', dict_paths['file_name'])
        # dict_paths['video_folder'].mkdir(parents=True, exist_ok=True)
        self.extension = '.pt' if self.deep else '.json'
        dict_paths['file_model'] = path.join(dict_paths['model_folder'], f'{dict_paths["file_name"]}{self.extension}')
        dict_paths['file_csv'] = path.join(dict_paths['data_folder'], f'{dict_paths["file_name"]}.csv')
        dict_paths['file_png'] = path.join(dict_paths['image_folder'], f'{dict_paths["file_name"]}.png')
        dict_paths['file_losses'] = path.join(dict_paths['image_folder'], f'{dict_paths["file_name"]}_losses.png')
        dict_paths['file_test'] = path.join(dict_paths['image_folder'], f'{dict_paths["file_name"]}_test.png')
        dict_paths['file_test_csv'] = path.join(dict_paths['data_folder'], f'{dict_paths["file_name"]}_test_csv.csv')
        dict_paths['file_compare_hist'] = path.join(dict_paths['image_folder'], f'comparison_hist.png')
        dict_paths['file_compare_rew'] = path.join(dict_paths['image_folder'], f'comparison_rew.png')
        return dict_paths

    def load_env(self, render_mode:str) -> None:
        '''
        Load environment. Render mode is different 
        for training (None) than for running (rgb_array). Render
        mode can only be set when instantiating the environment.
        '''
        # check if environment is given to be used
        if self.use_environment:
           return None
        if self.env_name in OWN_ENV_LIST:
            if self.env_parameters is not None:
              exec(f'self.environment = E.{self.env_name}(**self.env_parameters)')              
            else:
              exec(f'self.environment = E.{self.env_name}()')
            self.environment.render_mode = render_mode
        else:
          try:
            self.environment = gym.make(
                self.env_name, 
                render_mode=render_mode,
                **self.env_parameters
            )
          except:
            raise Exception(f'Environment {self.env_name} unknown.')

    def use_env(self, env:any) -> None:
       """Takes an environment for use in interaction"""
       assert(hasattr(env, 'step'))
       assert(hasattr(env, 'reset'))
       assert(hasattr(env, 'render'))
       assert(hasattr(env, 'render_mode'))
       assert(env.render_mode == 'rgb_array')
       self.environment = env
       self.use_environment = True

    def load_agent(self, from_file:bool=False):
        '''
        Load agent from name
        '''
        if self.agent_class == 'TabularAgents':
          line = f'self.agent = TableA.{self.agent_name}(self.agent_parameters)'
          self.deep = False
        elif self.agent_class == 'agentsCS':
          line = f'self.agent = ApproxQ.{self.agent_name}(self.agent_parameters)'
          self.deep = False
        elif self.agent_class == 'agentsNN':
          line = f'self.agent = ApproxNN.{self.agent_name}(self.agent_parameters)'
          self.deep = True
        elif self.agent_class == 'agentsPG':
          line = f'self.agent = ApproxP.{self.agent_name}(self.agent_parameters)'
        else:
           raise Exception(f'Agent class {self.agent_class} is unknown!')
        exec(line)
        if from_file:
          print(f'Loading agent from {self.dict_paths["file_model"]}')
          self.agent.load(file=self.dict_paths['file_model'])
    
    def save_agent(self):
        try:
            self.agent.save(file=self.dict_paths['file_model'])
        except Exception as e:
            print('\n\tAn error occurred:\n\t', e,'\n')
            pass

    def shutdown_agent_exploration(self) -> (float, np.ndarray):
        backup_epsilon = deepcopy(self.agent.epsilon)
        self.agent.epsilon = 0
        if hasattr(self.agent, 'policy'):
          backup_policy = deepcopy(self.agent.policy)
          for s in range(self.agent.nS):
            self.agent.update_policy(s)
        else:
          backup_policy = None
        return backup_epsilon, backup_policy

    def run(self, 
            from_file:bool=False,
            no_exploration:bool=False,
            visual:bool=True, 
            to_video:bool=False,
            sleep_time:float=0.3,
            num_rounds:int=200):
        '''
        Run the agent on the environment and displays the behavior.
        Agent does not learn.
        Input:
          - from_file (bool), if true, attemts to load the agent from file
          - no_exploration (bool), if true, makes epsilon = 0
          - visual (bool),
            True: displays the environment as in a video using environment render
            False: displays the behavioral data in the terminal step by step
          - to_video (bool),
            True: saves the rendering to a video file 
            False: displays the environment as in a video using environment render
          - sleep_time (float), determines the speed of the renderization
          - num_rounds (int), number of rounds to display
        '''
        # Load agent from name
        self.load_agent(from_file=from_file)
        # self.agent.debug = True # Uncomment for debugging
        if no_exploration:
          backup_epsilon, backup_policy = self.shutdown_agent_exploration()
        if visual and not to_video:
          '''
          To display the environment as in a video
          '''
          # Create environment
          # self.load_env(render_mode='human')
          self.load_env(render_mode='rgb_array')
          try:
            self.environment._max_episode_steps = num_rounds
          except:
             pass
          # Create episode
          episode = Episode(
              environment=self.environment,\
              env_name=self.env_name,\
              agent=self.agent,\
              model_name=self.agent_name,\
              num_rounds=num_rounds,\
              state_interpreter=self.state_interpreter
          )
          episode.sleep_time = sleep_time
          episode.renderize(to_video=False)
        elif to_video:
          '''
          To save to a video file
          '''
          # Create environment
          self.load_env(render_mode='rgb_array')
          try:
            self.environment._max_episode_steps = num_rounds
          except:
             pass
          # Create episode
          episode = Episode(
              environment=self.environment,\
              env_name=self.env_name,\
              agent=self.agent,\
              model_name=self.agent_name,\
              num_rounds=num_rounds,\
              state_interpreter=self.state_interpreter
          )
          episode.renderize(
              to_video=True,
              file=self.dict_paths['video_folder']
          )
        else:
          '''
          To display data information in the terminal
          '''
          # Create environment
          self.load_env(render_mode=None)
          try:
            self.environment._max_episode_steps = num_rounds
          except:
             pass
          # Create episode
          episode = Episode(
              environment=self.environment,\
              env_name=self.env_name,\
              agent=self.agent,\
              model_name=self.agent_name,\
              num_rounds=num_rounds,\
              state_interpreter=self.state_interpreter
          )
          df = episode.run(verbose=4, learn=False)
          self.data = df
        print('Number of rounds:', len(episode.agent.rewards) - 1)
        print('Total reward:', np.nansum(episode.agent.rewards))
        if no_exploration:
          self.agent.epsilon = backup_epsilon
          self.agent.policy = backup_policy
            
    def train(
            self, 
            num_rounds:int=200, 
            num_episodes:int=500, 
            from_file:bool=False
          ) -> None:
        '''
        Trains agent.
        '''
        # Load agent from name
        self.load_agent(from_file=from_file)
        # Create environment
        self.load_env(render_mode=None)
        try:
          self.environment._max_episode_steps = num_rounds
        except:
            pass
        # Create episode
        episode = Episode(
            environment=self.environment,\
            env_name=self.env_name,\
            agent=self.agent,\
            model_name=self.agent_name,\
            num_rounds=num_rounds,\
            state_interpreter=self.state_interpreter
        )
        # lengths = f'#states:{len(episode.agent.states)} -- #actions:{len(episode.agent.actions)} -- #rewards:{len(episode.agent.rewards)} -- #dones:{len(episode.agent.dones)}'
        # print('/>', lengths)
        # Train agent
        df = episode.simulate(
            num_episodes=num_episodes, 
            file=self.dict_paths['file_csv']
        )
        self.data = df
        print(f'Data saved to {self.dict_paths["file_csv"]}')
        # Save agent to file
        self.save_agent()
        print(f'Agent saved to {self.dict_paths["file_model"]}')
        # Plot results
        p =  Plot(df)
        if num_episodes == 1:
          p.plot_round_reward(file=self.dict_paths['file_png'])    
        else:
          p.plot_rewards(file=self.dict_paths['file_png']) 
        print(f'Plot saved to {self.dict_paths["file_png"]}')
        # Save losses if agent uses NN
        if hasattr(self.agent, 'NN'):
          if hasattr(self.agent.NN, 'losses'):
            losses = self.agent.NN.losses
            fig, ax = plt.subplots(figsize=(4,3.5))
            ax = sns.lineplot(x=range(len(losses)), y=losses)
            ax.set_xlabel("Epoch",fontsize=14)
            ax.set_ylabel("Loss",fontsize=14)
            plt.savefig(self.dict_paths['file_losses'], dpi=300, bbox_inches="tight")
        elif hasattr(self.agent, 'policy'):
          if hasattr(self.agent.policy, 'losses'):
            losses = self.agent.policy.losses
            fig, ax = plt.subplots(figsize=(4,3.5))
            ax = sns.lineplot(x=range(len(losses)), y=losses)
            ax.set_xlabel("Epoch",fontsize=14)
            ax.set_ylabel("Loss",fontsize=14)
            plt.savefig(self.dict_paths['file_losses'], dpi=300, bbox_inches="tight")

    def test(self, 
             no_exploration:bool=True,
             from_file:bool=True, 
             num_rounds:int=200, 
             num_episodes:int=100):
        '''
        Test the trained agent.
        '''
        # Load agent from name
        self.load_agent(from_file=from_file)
        if no_exploration:
          # Shutdown exploration
          backup_epsilon, backup_policy = self.shutdown_agent_exploration()
        # Create environment
        self.load_env(render_mode=None)
        try:
          self.environment._max_episode_steps = num_rounds
        except:
            pass
        # Create episode
        episode = Episode(
            environment=self.environment,\
            env_name=self.env_name,\
            agent=self.agent,\
            model_name=self.agent_name,\
            num_rounds=num_rounds,\
            state_interpreter=self.state_interpreter
        )
        # Run simulation
        df = episode.simulate(
            num_episodes=num_episodes, 
            learn=False
        )
        self.data = df
        df.to_csv(self.dict_paths['file_test_csv'])
        print(f'Data saved to {self.dict_paths["file_test_csv"]}')
        # Plot results
        p = Plot(df)
        p.plot_histogram_rewards(self.dict_paths['file_test'])
        print(f'Plot saved to {self.dict_paths["file_test"]}')
        if no_exploration:
          self.agent.epsilon = backup_epsilon
          if hasattr(self.agent, 'policy'):
            self.agent.policy = backup_policy
         
    def sweep(self, 
              parameter:str, 
              values:list, 
              num_rounds:int=200, 
              num_episodes:int=100,
              num_simulations:int=10):
        '''
        Runs a sweep over the specified parameter 
        with the specified values.
        '''
        # Load agent from name
        self.load_agent()
        # Creates environment
        self.load_env(render_mode=None)
        # Creates experiment
        experiment = Experiment(
            environment=self.environment,\
            env_name=self.env_name,\
            num_rounds=num_rounds,\
            num_episodes=num_episodes,\
            num_simulations=num_simulations,\
            state_interpreter=self.state_interpreter
        )
        # Run sweep
        experiment.run_sweep1(
            agent=self.agent, \
            name=self.agent_name, \
            parameter=parameter, \
            values=values, \
            measures=['reward']
        )
        self.data = experiment.data
        # Plot results
        p = Plot(experiment.data)
        print('Plotting...')
        p.plot_rewards(self.dict_paths['file_compare_rew'])
        print(f'Plot saved to {self.dict_paths["file_compare_rew"]}')
        
    def compare_test(self, 
                     agent_vs_name:str,
                     agent_vs_parameters:Dict,
                     num_rounds:int=200, 
                     num_episodes:int=100):
        '''
        Runs a comparison of two agents
        over an environment.
        Agents are loaded from file.
        '''
        # Load agent 1
        self.load_agent(from_file=True)
        self.shutdown_agent_exploration()
        agent1 = deepcopy(self.agent)
        # Load vs agent
        backup_agent_name = self.agent_name
        backup_agent_parameters = deepcopy(self.agent_parameters)
        self.agent_name = agent_vs_name
        self.agent_parameters = agent_vs_parameters
        self.consolidate_folders()
        try:
          self.load_agent(from_file=True)
        except Exception as e:
          print(e)
          print(f'An agent of class {agent_vs_name} is required.\nRun a performer on such an agent first.') 
        self.shutdown_agent_exploration()
        agent2 = deepcopy(self.agent)
        self.agent_name = backup_agent_name
        self.agent_parameters = backup_agent_parameters
        self.consolidate_folders()
        # Create environment
        self.load_env(render_mode=None)
        # Create experiment
        experiment = Experiment(
            environment=self.environment,\
            env_name=self.env_name,\
            num_rounds=num_rounds,\
            num_episodes=num_episodes,\
            num_simulations=1,\
            state_interpreter=self.state_interpreter
        )
        # Run sweep
        experiment.run_experiment(
            agents=[agent1, agent2], \
            names=[self.agent_name, agent_vs_name], \
            measures=['hist_reward'],\
            learn=False
        )
        self.data = experiment.data
        # Plot results
        p = Plot(experiment.data)
        print('Plotting...')
        p.plot_histogram_rewards(self.dict_paths['file_compare_hist'])
        print(f'Plot saved to {self.dict_paths["file_compare_hist"]}')

