import gym
from gym import spaces
import numpy as np

import time
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import os.path

url = "http://2048game.com"

MAX_REWARD = float("inf")

class Game2048Env(gym.Env):
	"""Custom Environment that follows gym interface"""
	metadata = {'render.modes': ['human']}

	def __init__(self, driver):
		super(Game2048Env, self).__init__()
		self.reward_range = (-MAX_REWARD, MAX_REWARD)
		self.driver = driver
		self.score = 0
		self.high_score = 0
		self.tile_best = 0

		self.action_space = spaces.Discrete(4)
		self.idle = 0
		self.current_step = 0
		self.meanings = [Keys.ARROW_DOWN, Keys.ARROW_UP, Keys.ARROW_LEFT, Keys.ARROW_RIGHT]
		self.observation_space = spaces.Box(low=np.array([0 for i in range(16)]), high=np.array([16 for i in range(16)])) 
	                

	def step(self, action):
		# Execute one time step within the environment
		self._take_action(action)

		self.current_step += 1
		done = False

		try:
			self.get_score()
			obs = self._next_observation(action)
		except:
			obs = self._next_observation(action)
			done = True
			return obs, 0, done, {}


		self.tile_best = max(self.tile_best, self.table[15])


		if self.table == self.oldtable:
			self.idle += 1
			self.reward = -(self.idle**2)
			# print(self.reward)
			return obs, -(self.reward**2), done, {}
		else:
			self.idle = 0

		reward = 2 ** self.table[15]

		self.reward = reward


		return obs, reward, done, {}

	def _take_action(self, action):
		# action is a number. move left, right, up, down.
		self.elem.send_keys(self.meanings[action])
		# time.sleep(0.5)

	
	def reset(self):
		# Reset the state of the environment to an initial state
		self.score = 0
		self.reward = 0
		self.current_step = 0
		self.table = [0 for i in range(16)]
		self.oldtable = [0 for i in range(16)]

		self.idle = 0
		self.last_idle_actions = []
		self.tile_best = 0
		# self.meanings = [Keys.ARROW_DOWN, Keys.ARROW_UP, Keys.ARROW_LEFT, Keys.ARROW_RIGHT]

		self.driver.get(url)
		element = self.driver.find_element_by_tag_name("a")
		element.click()
		self.elem = self.driver.find_element_by_tag_name("html")

		return self._next_observation(0)

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
		return self.table


	def render(self, mode='human', close=False):
		# Render the environment to the screen
		print(self.score, self.reward)


	def get_score(self): # update score
		storage = self.driver.execute_script("return window.localStorage.gameState;")
		score = int(re.search("\"score\":([0-9]*)", storage).group(1))
		self.score = score

	def close_driver(self):
		self.driver.close()
