import gym
from gym import spaces
import numpy as np

import time
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import os.path

url = "file:///Users/kaankatircioglu/Desktop/push_here/2048bot/2048/index.html"

MAX_REWARD = float("inf")


class Game2048Env(gym.Env):
	"""Custom Environment that follows gym interface"""
	metadata = {'render.modes': ['human']}

	def __init__(self, driver):
		super(Game2048Env, self).__init__()
		self.reward_range = (-MAX_REWARD, MAX_REWARD)
		self.driver = driver
		self.meanings = [Keys.ARROW_DOWN, Keys.ARROW_UP, Keys.ARROW_LEFT, Keys.ARROW_RIGHT]


		self.action_space = spaces.Discrete(4)
		self.current_step = 0
		self.score = 0

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



		try:
			self.get_score()
			obs = self._next_observation(action)
		except:
			# Ugly way but works fine
			exit(0)
		# 	obs = self._next_observation(action)
		# 	print("hello")
		# 	driver = None
		# 	return obs, 2000, True, {}

		if not self.canMove():
			exit(0)
			print("hi")
			return obs, 2000, True, {}


		reward = 2 ** self.table[15] + 0.1 * (2 ** self.table[11])
		print("hi", self.table)


		if self.idle > 10:
			exit(0)
			return obs, -2000, True, {}


		self.reward = reward

		return obs, reward, done, {}


	# move in real game, alter the api's table
	def _take_action(self, action):
		# action is a number. move left, right, up, down.
		self.elem.send_keys(self.meanings[action])
		

	
	def reset(self):
		# Reset the state of the environment to an initial state
		self.current_step = 0
		self.last_action = 0
		self.reward = 0
		self.idle = 0
		self.score = 0

		self.table = [0 for i in range(16)]
		self.oldtable = [0 for i in range(16)]

		self.driver.get(url)
		element = self.driver.find_element_by_tag_name("a")
		element.click()
		self.elem = self.driver.find_element_by_tag_name("html")

		return self._next_observation(0)

	# action is unnecessary but left it
	def _next_observation(self, action):
		storage = str(self.driver.execute_script("return window.localStorage.gameState;"))
		grid = re.findall(r'(null|e":[0-9]*)', storage)

		if grid == []:
			return self.table

		for i in range(16):
			if grid[i+1] == "null":
				self.oldtable[i] = self.table[i]
				self.table[i] = 0
			else:
				self.oldtable[i] = self.table[i]
				self.table[i] = int(grid[i+1][3:]).bit_length() - 1

		self.idle = self.idle + 1 if self.oldtable == self.table else 0
		print(self.table)
		return [[self.idle, 0, 0, 0], 
		[self.table[0], self.table[4], self.table[8], self.table[12]], 
		[self.table[1], self.table[5], self.table[9], self.table[13]],
		[self.table[2], self.table[6], self.table[10], self.table[14]],
		[self.table[3], self.table[7], self.table[11], self.table[15]]]


	def render(self, mode='human', close=False):
		# Render the environment to the screen
		print(self.score, self.reward)


	def get_score(self): # update score
		storage = self.driver.execute_script("return window.localStorage.gameState;")
		score = int(re.search("\"score\":([0-9]*)", storage).group(1))
		self.score = score


	def _where_empty(self):
		'''return where is empty in the board'''
		return list(zip(*np.where(self.table == 0)))


	def canMove(self):
			"""
			test if a move is possible
			"""
			if self._where_empty():
				return True

			for y in range(4):
				for x in range(4):
					c = self.table[y*4 + x]
					if (x < 3 and self.table[y*4 + x+1]) \
					   or (y < 3 and c == self.table[y*4 + 4+ x]):
						return True

			return False