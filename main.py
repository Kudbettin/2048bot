import gym
import json
import datetime as dt

from selenium import webdriver

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

from Game2048Env import Game2048Env

import os.path
import re
import os



model_name = "ppo2_2048"
timesteps = 10000

driver = webdriver.Firefox(executable_path="./geckodriver")
# The algorithms require a vectorized environment to run
env = DummyVecEnv([lambda: Game2048Env(driver)])


if not os.path.exists(model_name + ".pkl"):
	model = PPO2(MlpPolicy, env, verbose=1)
else:
	model = PPO2.load("ppo2_2048")
	model.set_env(env)	

model.learn(total_timesteps=timesteps)
model.save(model_name)



##### LOG ######

if not os.path.exists("log_ppo2.txt"):
	file = open("log_ppo2.txt", 'w+')
	file.write("cumulative_timesteps: 0, highest score: 0\n")
else:
	file = open("log_ppo2.txt", 'r+')


log = file.readline()
numbers = re.findall('[0-9]+', log)
numbers[0] = str(timesteps + int(numbers[0]))

file.truncate(0)

file.write("cumulative_timesteps: " + numbers[0] +", highest score: " + numbers[1] + "\n")

file.close()

##### END of LOG #######


# os.system("say 'training complete'")

driver.quit()
