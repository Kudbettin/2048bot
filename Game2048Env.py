import gym
from gym import spaces
import numpy as np

import time
import re

import os.path

from term2048 import Game



MAX_REWARD = float("inf")
# MAX_STEPS = 200

class Game2048Env(gym.Env):
	"""Custom Environment that follows gym interface"""
	metadata = {'render.modes': ['human']}

	def __init__(self):
		super(Game2048Env, self).__init__()
		self.reward_range = (-MAX_REWARD, MAX_REWARD)
		self.game = Game(size=4)

		self.action_space = spaces.Discrete(4)
		self.current_step = 0

		self.last_action = 0
		self.forced_actions = [0, 2, 1, 3]
		# self.observation_space = spaces.Box(low=np.array([0 for i in range(16)]), high=np.array([16 for i in range(16)])) 
		low_list = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]# [0] + [[0, 0, 0, 0] for i in range(4)]
		high_list = [[11, 0, 0, 0], [16, 16, 16, 16], [16, 16, 16, 16], [16, 16, 16, 16], [16, 16, 16, 16]]# [6] + [[16, 16, 16, 16] for i in range(4)]
		self.observation_space = spaces.Box(low=np.array(low_list), high=np.array(high_list)) 
	                

	def step(self, action):
		# Execute one time step within the environment
		self._take_action(action)

		self.current_step += 1
		done = False

		obs = self._next_observation(action)

		if self.game.end:
			done = True
			return obs, 2000, True, {}

		# if self.game.board[3][3] != 0 and self.game.score > 0 \
		# 		and self.game.score > self.game.board[3][3]:
		# 	return obs, -2000, True, {}

		
		reward = 2 ** self.table[3][3] + 0.1 * (2 ** self.table[3][2])

		# reward = [[self.table[i][j] for j in range(4)] for i in range(4)]

		# if self.game.idle > 0:
		# 	reward = - 1 * self.game.idle
		if self.game.idle > 10:
			return obs, -2000, True, {}


		self.reward = reward

		return obs, reward, done, {}

	def _take_action(self, action):
		# action is a number. move left, right, up, down.
		self.last_action = action
		self.game.move(action)


		# for act in self.forced_actions:
		# 	self.game.move(act)
		# 	if self.game.idle > 0:
		# 		break
		

	
	def reset(self):
		# Reset the state of the environment to an initial state
		self.current_step = 0
		self.last_action = 0
		self.reward = 0
		self.game = Game(size=4)

		return self._next_observation(0)

	def _next_observation(self, action):

		self.table = [[int(col).bit_length() - 1 if col != 0 else 0 for col in row] for row in self.game.board]
		return [[self.game.idle, 0, 0, 0], self.table[0], self.table[1], self.table[2], self.table[3]]


	def render(self, mode='human', close=False):
		# Render the environment to the screen
		printable = self.game.__str__() + "\n" + \
		"last action:" + str(self.last_action) + "\n" \
		"table: " + str(self.table) + "\n" \
		"reward:" + str(self.reward) + "\n" \
		+ str(self.current_step) + "\n"

		print(printable)



