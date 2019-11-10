import os
import re
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from term2048 import Game


url = "file://" + os.path.dirname(os.path.abspath(__file__)) + "/2048/index.html"
print(url)
meanings = [Keys.ARROW_LEFT, Keys.ARROW_DOWN, Keys.ARROW_RIGHT, Keys.ARROW_UP]

directions = ["left", "down", "right", "up"]

def main():
	table = [0 for i in range(16)]
	driver = webdriver.Firefox(executable_path="./geckodriver")
	driver.get(url)
	element = driver.find_element_by_tag_name("a")
	element.click()
	elem = driver.find_element_by_tag_name("html")

	game = Game(size = 4, enable_rewrite_board = True)
	game.board = observation(driver, table)
	# print(game)

	while True:
		pile = [0, 0, 0, 0]

		for i in range(4):
			reward, moves = calculate_moves(game, 3)
			if moves is not None:
				pile[moves[-1]] += 1

		if max(pile) == 0:
			reward, moves = calculate_moves(game, 4)

		try:
			game.move(pile.index(max(pile)))
			elem.send_keys(meanings[pile.index(max(pile))])
			game.board = observation(driver, table)
			# print(type(observation(driver)))
			# print(observation(driver))
		except:
			print("Game is probably over")
			break
		# print(game)

	# print(game)


def observation(driver, table):
		storage = str(driver.execute_script("return window.localStorage.gameState;"))
		grid = re.findall(r'(null|e":[0-9]*)', storage)
		
		if grid == []:
			return table

		for i in range(16):
			if grid[i+1] == "null":
				# oldtable[i] = table[i]
				table[i] = 0
			else:
				# oldtable[i] = table[i]
				table[i] = int(grid[i+1][3:]).bit_length() - 1

		# idle = idle + 1 if oldtable == table else 0
		# print(table)
		return np.array([[table[0], table[4], table[8], table[12]], 
		[table[1], table[5], table[9], table[13]],
		[table[2], table[6], table[10], table[14]],
		[table[3], table[7], table[11], table[15]]])


def calculate_moves(game, n, reward_multiplier=1):
	if n == 0:
		table = np.matrix([[int(col).bit_length() - 1 if col != 0 else 0 for col in row] for row in game.board])
		reward = game.board[3][3]-(table.sum())*reward_multiplier
		reward += heruistics(table, game.score)
		return reward, []

	current_board = game.board

	best_reward = -float("inf")
	best_move = None
	best_moves = None

	for move in range(4):
		game.move(move)

		if game.idle or game.end:
			game.board = current_board
			continue

		reward, moves = calculate_moves(game, n-1, reward_multiplier)

		if reward is None:
			game.board = current_board
			continue

		if reward > best_reward:
			best_reward = reward
			best_move = move
			best_moves = moves

		game.board = current_board

	if best_reward == -float("inf"):
		return None, None

	best_moves.append(best_move)
	return best_reward, best_moves




# Add some heruistics tactics to the decision
# Returns value/reward of the given table
# very naive
def heruistics(board, biggest):
	table = np.asarray(board).reshape(-1)
	edges = np.array([0, 1, 2, 3, 4, 7, 8, 11, 12, 13, 14, 15])


	edge_score = 0
	indices = np.where(table==np.max(table))
	for i in indices:
		if i in edges:
			edge_score += 1

	empty_score = 0
	for tile in table:
		if tile == 0:
			empty_score += 1

	
	monotonic_score = 0

	d = np.diff(board[0])
	if np.all(d <= 0) or np.all(d >= 0):
		monotonic_score += 2 * np.sum(board[0])

	d = np.diff(board[3])
	if np.all(d <= 0) or np.all(d >= 0):
		monotonic_score += 2 * np.sum(board[3])

	d = np.diff(board[1])
	if np.all(d <= 0) or np.all(d >= 0):
		monotonic_score += np.sum(board[1])

	d = np.diff(board[2])
	if np.all(d <= 0) or np.all(d >= 0):
		monotonic_score += np.sum(board[2])


	d = np.diff(board[:, 0])
	if np.all(d <= 0) or np.all(d >= 0):
		monotonic_score += 2 * np.sum(board[:, 0])

	d = np.diff(board[:, 3])
	if np.all(d <= 0) or np.all(d >= 0):
		monotonic_score += 2 * np.sum(board[:, 3])

	d = np.diff(board[:, 1])
	if np.all(d <= 0) or np.all(d >= 0):
		monotonic_score += np.sum(board[:, 1])

	d = np.diff(board[:, 2])
	if np.all(d <= 0) or np.all(d >= 0):
		monotonic_score += np.sum(board[:, 2])

	# print(edge_score*biggest, empty_score*10, monotonic_score)
	return edge_score*biggest + empty_score*10 + monotonic_score





if __name__ == '__main__':
	main()



