'''A numpy-based 2048 game core implementation.'''

import numpy as np


class Game:

    def __init__(self, size=4, rate_2=0.9, enable_rewrite_board=False):
        '''

        :param size: the size of the board
        :param rate_2: the probability of the next element to be 2 (otherwise 4)
        '''
        self.size = size
        self.__rate_2 = rate_2

        self.__board = np.zeros((self.size, self.size))
        # initilize the board (with 2 entries)
        self._maybe_new_entry()
        self._maybe_new_entry()

        self.enable_rewrite_board = enable_rewrite_board
        # assert not self.end
        self.__end = False

        self.old_board = np.zeros((self.size, self.size))
        self.fake_board = np.zeros((self.size, self.size))

        self.idle = 0

    def move(self, direction):
        '''
        direction:
            0: left
            1: down
            2: right
            3: up
        '''
        self.old_board = np.copy(self.__board)
        # treat all direction as left (by rotation)
        board_to_left = np.rot90(self.board, -direction)
        for row in range(self.size):
            core = self._merge(board_to_left[row])
            board_to_left[row, :len(core)] = core
            board_to_left[row, len(core):] = 0

        # rotation to the original
        self.__board = np.rot90(board_to_left, direction)

        if not (self.old_board == self.__board).all():
            self._maybe_new_entry()
            self.idle = 0
            # print("should add")
        else:
            self.idle += 1
            # print("shouldn't add")

        if not self.canMove():
            self.__end = True

    def fake_move(self, direction, fake_board):
        '''
        direction:
            0: left
            1: down
            2: right
            3: up
        '''

        # treat all direction as left (by rotation)
        board_to_left = np.rot90(self.board, -direction)
        for row in range(self.size):
            core = _merge(board_to_left[row])
            board_to_left[row, :len(core)] = core
            board_to_left[row, len(core):] = 0

        # rotation to the original
        self.fake_board = np.rot90(board_to_left, direction)

        idle = 1
        dead = 0
        if not (self.__board == self.fake_board).all():
            # self._maybe_new_entry() # make this affect the fake board
            idle = 0
            # print("should add")

        if not self.canMove():
            dead = 1

        reward = self.fake_board[3][3] + 0.1 * (self.fake_board[3][2])

        return dead, idle, reward

    def fake_moves(self):
        observation = np.zeros((4, 3))

        for i in range(4):
            observation[i][0], observation[i][1], observation[i][2] = self.fake_move(i, self.fake_board)

        return observation


    def __str__(self):
        board = "State:"
        for row in self.board:
            board += ('\t' + '{:8d}' *
                      self.size + '\n').format(*map(int, row))
        board += "Score: {0:d}".format(self.score)
        return board

    @property
    def board(self):
        '''`NOTE`: Setting board by indexing,
        i.e. board[1,3]=2, will not raise error.'''
        return self.__board.copy()

    @board.setter
    def board(self, x):
        if self.enable_rewrite_board:
            assert self.__board.shape == x.shape
            self.__board = x.astype(self.__board.dtype)
        else:
            print("Disable to rewrite `board` manually.")

    @property
    def score(self):
        return int(self.board.max())

    @property
    def end(self):

        return self.__end

    def _maybe_new_entry(self):
        '''maybe set a new entry 2 / 4 according to `rate_2`'''
        where_empty = self._where_empty()
        if where_empty:
            selected = where_empty[np.random.randint(0, len(where_empty))]
            self.__board[selected] = \
                2 if np.random.random() < self.__rate_2 else 4
            self.__end = False
        else:
            self.__end = True

    def _where_empty(self):
        '''return where is empty in the board'''
        return list(zip(*np.where(self.board == 0)))


    def canMove(self):
            """
            test if a move is possible
            """
            if self._where_empty():
                return True

            for y in range(self.size):
                for x in range(self.size):
                    c = self.__board[y][x]
                    if (x < self.size-1 and c == self.__board[y][x+1]) \
                       or (y < self.size-1 and c == self.__board[y+1][x]):
                        return True

            return False

    def _merge(self, row):
        '''merge the row, there may be some improvement'''
        non_zero = row[row != 0]  # remove zeros
        core = [None]
        for elem in non_zero:
            if core[-1] is None:
                core[-1] = elem
            elif core[-1] == elem:
                core[-1] = 2 * elem
                core.append(None)
            else:
                core.append(elem)
        if core[-1] is None:
            core.pop()
        return core

