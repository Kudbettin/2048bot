import gym
import json
import datetime as dt

from stable_baselines.common.vec_env import DummyVecEnv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from testEnv import Game2048Env

import os.path
import re
import os

import sys

from tensorflow.nn import leaky_relu


model_list = ["A2C", "ACER", "ACKTR", "DDPG", "DQN", "GAIL", "HER", "PPO1", "PPO2", "SAC", "TRPO"]

if len(sys.argv) != 2:
	print("Invalid arguments. Usage: python3 main.py [model_index]") 
	for i in range(len(model_list)):
		print(model_list[i] + ":", i)
	exit(1)



# TRPO = imp.load_source("stable_baselines", )
_model = __import__("stable_baselines", globals(), locals(), [model_list[int(sys.argv[1])]], 0)
MODEL = getattr(_model, model_list[int(sys.argv[1])])
# exit(1)

if model_list[int(sys.argv[1])] == "DQN":
	from stable_baselines.deepq.policies import MlpPolicy
else:
	from stable_baselines.common.policies import MlpPolicy


model_name = "weights/" + model_list[int(sys.argv[1])] + "_2048"


driver = webdriver.Firefox(executable_path="./geckodriver")
env = DummyVecEnv([lambda: Game2048Env(driver)])

policy_kwargs = dict(act_fun=leaky_relu, net_arch=[32, 16, 8])


if not os.path.exists(model_name + ".pkl"):
	model = MODEL(MlpPolicy, env, verbose=1, policy_kwargs=policy_kwargs)
	print("Testing on untrained model")
else:
	model = MODEL.load(model_name)
	model.set_env(env)	


# Test the model
obs = env.reset()
dones = [False]
while not dones[0]:
# for i in range(20):
    action, _states = model.predict(obs)
    # print("action, _states: ", action, _states)
    obs, rewards, dones, info = env.step(action)
    # env.render()
    # print(dones)

# driver.close()

# os.system("say 'testing complete'")