import gym
import json
import datetime as dt

from selenium import webdriver

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

from TestEnv import Game2048Env

import os.path
import re
import os



model_name = "ppo2_2048"


driver = webdriver.Firefox(executable_path="./geckodriver")
# The algorithms require a vectorized environment to run
env = DummyVecEnv([lambda: Game2048Env(driver)])


if not os.path.exists(model_name + ".pkl"):
	model = PPO2(MlpPolicy, env, verbose=1)
	print("testing on untrained model")
else:
	model = PPO2.load("ppo2_2048")
	model.set_env(env)	



##### END of LOG #######

obs = env.reset()
for i in range(2000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()

driver.quit()

os.system("say 'testing complete'")