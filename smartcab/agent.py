#!/usr/bin/python2.7

import pygame
import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from collections import defaultdict
import operator

def initTable(state, table, valid_env):
	if state not in table:
        	table[state]={}
        	for actions in valid_env:
        		table[state][actions]=0

def alphaTime(N):
    return float(1)/(1+float(N))
    
def epsilonTime(N):
    value = 1-N
    if value >= 0:
    	return value
    else:
    	return 0	

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # Initialize any additional variables here
	self.timeAlpha = 0.1
	self.timeEpsilon = 0
	self.Q_table = defaultdict(dict)
	self.R_table = defaultdict(dict)
	self.alpha = 0
	self.gamma = 0.5
	self.epsilon = 1

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # Prepare for a new trip; reset any variables here, if required
	self.timeAlpha = 0.1

    def update(self, t):
        
        self.alpha = alphaTime(self.timeAlpha)
        self.epsilon = epsilonTime(self.timeEpsilon)
         
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator       
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
             
        # Update state 
        self.state = (inputs['light'], inputs['oncoming'], inputs['left'], inputs['right'], self.next_waypoint)
        current_state = self.state
        print current_state
        
        # Initialize state
        initTable(current_state, self.Q_table, self.env.valid_actions)
        
        # Select action according to your policy 
        if random.random() < self.epsilon:
            	action = random.choice(self.env.valid_actions)   	
	else:
		maxActions = [key for key, value in self.Q_table[current_state].items() if value == max(self.Q_table[current_state].values())]
		action = random.choice(maxActions) 
	print "best action = ", action
	print "actions available = ", self.Q_table[current_state].items()	
        
        # Execute action and get reward
        reward = self.env.act(self, action) 
        
        self.R_table[current_state][action] = reward
        
        # Update state
	self.state = (inputs['light'], inputs['oncoming'], inputs['left'], inputs['right'], self.next_waypoint)
	#self.state = convState(inputs, deadline, self.next_waypoint)
        next_state = self.state 
        
        # Initialize state
        initTable(next_state, self.Q_table, self.env.valid_actions)
        
        # Learn policy based on state, action, reward
        if random.random() < self.epsilon:
            	next_action = random.choice(self.Q_table[next_state].values())	
	else:
		maxActions = [value for key, value in self.Q_table[next_state].items() if value == max(self.Q_table[next_state].values())]
		next_action = random.choice(maxActions)

	# Q-Learning implementation
        self.Q_table[current_state][action]=((1-self.alpha) * self.Q_table[current_state][action])+(self.alpha*(self.R_table[next_state][action]+(self.gamma*next_action)))          
        
        # Update time
	self.timeAlpha += 0.1
	self.timeEpsilon += 0.05
	
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
