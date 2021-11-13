import time
from Board import Board
from BoardBuilder import BoardBuilder
import numpy as np

class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3

	def __init__(self, recommend = True):
		self.initialize_game()
		self.recommend = recommend

	def initialize_game(self):
		self.board = BoardBuilder().boardSize().blocks().coordinates().winningSize().build()
		self.d1 = int(input('Enter the max depth for player one: '))
		self.d2 = int(input('Enter the max depth for player two: '))
		# Player X always plays first
		self.player_turn = 'X'

	def test1(self):
		self.board = Board(3, 0, 3, list())
		self.board.current_state = [['O', 'X', 'O'],
				                      ['X', 'X', 'O'],
				                      ['X', '.', '.']]
		# self.board.current_state = [['X', 'O', 'X','O','X'],
		# 							['.', 'O', '.','.','.'],
		# 							['.', 'X', 'X','.','.'],
		# 							['.', 'X', '.','X','.'],
		# 							['.', 'X', '.','.','X']]
		self.draw_board()
		self.check_end()

	def draw_board(self):
		print()
		for y in range(0, self.board.board_size):
			for x in range(0, self.board.board_size):
				print(F'{self.board.current_state[x][y]}', end="")
			print()
		print()
		
	def is_valid(self, px, py):
		if px < 0 or px > self.board.board_size - 1 or py < 0 or py > self.board.board_size - 1:
			return False
		elif self.board.current_state[px][py] != '.':
			return False
		else:
			return True

	def is_end(self):
		# Vertical win
		for i in range(0, self.board.board_size):
			result = self.checkStreak(self.board.current_state[i])
			if result:
				return result
		# Horizontal win
		for i in range(0, self.board.board_size):
			result = self.checkStreak([row[i] for row in self.board.current_state])
			if result:
				return result
		# Diagonal win
		boardArray = np.array(self.board.current_state)
		diags = [boardArray[::-1,:].diagonal(i) for i in range(-boardArray.shape[0]+1,boardArray.shape[1])]
		diags.extend(boardArray.diagonal(i) for i in range(boardArray.shape[1]-1,-boardArray.shape[0],-1))
		
		for diag in diags:
			if len(diag) >= self.board.winning_size:
				result = self.checkStreak(diag.tolist())
			if result:
				return result
		# Is whole board full?
		for i in range(0, self.board.board_size):
			for j in range(0, self.board.board_size):
				# There's an empty field, we continue the game
				if (self.board.current_state[i][j] == '.'):
					return None
		# It's a tie!
		return '.'

	def check_end(self):
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
			#self.initialize_game()
		return self.result

	def input_move(self):
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = int(input('enter the x coordinate: '))
			py = int(input('enter the y coordinate: '))
			if self.is_valid(px, py):
				return (px,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def minimax(self, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, self.board.board_size):
			for j in range(0, self.board.board_size):
				if self.board.current_state[i][j] == '.':
					if max:
						self.board.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.board.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.board.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, alpha=-2, beta=2, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, self.board.board_size):
			for j in range(0, self.board.board_size):
				if self.board.current_state[i][j] == '.':
					if max:
						self.board.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.board.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(alpha, beta, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.board.current_state[i][j] = '.'
					if max: 
						if value >= beta:
							return (value, x, y)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y)
						if value < beta:
							beta = value
		return (value, x, y)

	def play(self,algo=None,player_x=None,player_o=None):
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		while True:
			self.draw_board()
			print('Going Again')
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(max=False)
				else:
					(_, x, y) = self.minimax(max=True)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False)
				else:
					(m, x, y) = self.alphabeta(max=True)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
			self.board.current_state[x][y] = self.player_turn
			self.switch_player()

	def checkStreak(self, array):
		count = 1
		for i in range(len(array)-1):
			if (not(array[i] == '.' or array[i] == '*') and array[i] == array[i+1]):
				count += 1
				if (count == self.board.winning_size):
					return array[i]
			else:
				count = 1
		return None
