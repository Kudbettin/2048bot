import gym
import json
import datetime as dt

from stable_baselines.common.vec_env import DummyVecEnv

from Game2048Env import Game2048Env

import os.path
import re
import os

import sys

from tensorflow.nn import leaky_relu


model_list = ["A2C", "ACER", "ACKTR", "DDPG", "DQN", "GAIL", "HER", "PPO1", "PPO2", "SAC", "TRPO"]

if len(sys.argv) != 3:
	print("Invalid arguments. Usage: python3 main.py [model_index] [timesteps]") 
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
# log_file = "logs/" + "log_" + model_list[int(sys.argv[1])] + ".txt"
timesteps = int(sys.argv[2])


# The algorithms require a vectorized environment to run
env = DummyVecEnv([lambda: Game2048Env()])

policy_kwargs = dict(act_fun=leaky_relu, net_arch=[32, 16, 8])

# The latter is for further trainings
if True:# not os.path.exists(model_name + ".pkl"):
	model = MODEL(MlpPolicy, env, policy_kwargs = policy_kwargs,verbose=1)
else:
	model = MODEL.load(model_name)
	model.set_env(env)	

model.learn(total_timesteps=timesteps)
model.save(model_name)


# Test the model
obs = env.reset()
dones = [False]
while not dones[0]:
    action, _states = model.predict(obs)
    print("action, _states: ", action, _states)
    obs, rewards, dones, info = env.step(action)
    env.render()
    print(dones)


# os.system("say 'training complete'")
