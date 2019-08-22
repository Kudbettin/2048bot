import numpy as np

from term2048 import Game


directions = ["left", "down", "right", "up"]

def main():
	game = Game(size = 4, enable_rewrite_board = True)
	print(game)

	while True:
		pile = [0, 0, 0, 0]

		for i in range(4):
			reward, moves = calculate_moves(game, 2)
			if moves is not None:
				pile[moves[-1]] += 1

		if max(pile) == 0:
			reward, moves = calculate_moves(game, 1)

		game.move(pile.index(max(pile)))
		print(game)

		if game.end:
			break

	print(game)




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



