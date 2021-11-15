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
		self.visited = 0

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
		# 							['.', 'O', '*','*','.'],
		# 							['.', 'X', 'X','.','.'],
		# 							['.', 'X', '.','X','.'],
		# 							['*', 'X', '*','.','X']]
		self.draw_board()
		print(self.e2())

	def draw_board(self):
		print("  ", end="")
		for i in range(self.board.board_size):
			print(chr(i + 65), end="")
		print('\n +', end="")
		for i in range(self.board.board_size):
			print('-', end="")
		print()
		for y in range(0, self.board.board_size):
			print(f'{y}|', end="")
			for x in range(0, self.board.board_size):
				print(F'{self.board.current_state[x][y]}', end="")
			print()
		print()
	#TODO Should we put it in the same method?
	def draw_board_file(self,file):
		file.write("  ")
		for i in range(self.board.board_size):
			file.write(chr(i + 65))
		file.write('\n +')
		for i in range(self.board.board_size):
			file.write('-')
		file.write('\n')
		for y in range(0, self.board.board_size):
			file.write(f'{y}|')
			for x in range(0, self.board.board_size):
				file.write(F'{self.board.current_state[x][y]}')
			file.write('\n')
		file.write('\n')
		
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
			px = int(ord(input('enter the x coordinate: ')) - 65)
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

	def minimax(self, maxdepth, max=False):
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
		if maxdepth == 0:
			self.visited +=1
			if self.player_turn == 'X':
				return self.e1()
			else:
				return self.e1() # change for e2
				
		elif result == 'X':
			self.visited +=1
			return (-1, x, y)
		elif result == 'O':
			self.visited +=1
			return (1, x, y)
		elif result == '.':
			self.visited +=1
			return (0, x, y)
		for i in range(0, self.board.board_size):
			for j in range(0, self.board.board_size):
				if self.board.current_state[i][j] == '.':
					if max:
						self.board.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(self.d2-1,max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.board.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(self.d1-1,max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.board.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, maxdepth, alpha=-2, beta=2, max=False):
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
		if maxdepth == 0:
			self.visited +=1
			if self.player_turn == 'X':
				return self.e1()
			else:
				return self.e1() #change for e2
		if result == 'X':
			self.visited +=1
			return (-1, x, y)
		elif result == 'O':
			self.visited +=1
			return (1, x, y)
		elif result == '.':
			self.visited +=1
			return (0, x, y)
		for i in range(0, self.board.board_size):
			for j in range(0, self.board.board_size):
				if self.board.current_state[i][j] == '.':
					if max:
						self.board.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(self.d2 - 1, alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.board.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(self.d1 -1, alpha, beta, max=True)
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
		n = self.board.board_size
		b = self.board.number_blocks
		s = self.board.winning_size
		t = 5
		bloc_list = list()
		with open(F'gameTrace-{n}{b}{s}{t}.txt','a') as file:
			file.write(F'n={n} b={b} s={s} t={t}\n')
			for i in range(0, self.board.board_size):
				for j in range(0, self.board.board_size):
					if (self.board.current_state[i][j] == '*'):
						bloc_list.append((i,j))
			file.write(F'blocs={bloc_list}\n')
			if algo == None:
				algo = self.ALPHABETA
			if player_x == None:
				player_x = self.HUMAN
				file.write(F'Player 1: HUMAN\n')
			else:
				file.write(F'Player 1: AI d={self.d1} e1(regular)\n')
			if player_o == None:
				player_o = self.HUMAN
				file.write(F'Player 2: HUMAN\n')
			else:
				file.write(F'Player 2: AI d={self.d2} e2(defensive)\n')

			while True:
				self.draw_board()
				self.draw_board_file(file)
				print('Going Again')
				if self.check_end():
					return
				start = time.time()
				if algo == self.MINIMAX:
					if self.player_turn == 'X':
						(_, x, y) = self.minimax(self.d1, max=False)
					else:
						(_, x, y) = self.minimax(self.d2, max=True)
				else: # algo == self.ALPHABETA
					if self.player_turn == 'X':
						(m, x, y) = self.alphabeta(self.d1, max=False)
					else:
						(m, x, y) = self.alphabeta(self.d2, max=True)
				end = time.time()
				if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
						if self.recommend:
							file.write(F'Evaluation time: {round(end - start, 7)}s')
							file.write(F'Recommended move: x = {x}, y = {y}')
							print(F'Evaluation time: {round(end - start, 7)}s')
							print(F'Recommended move: x = {x}, y = {y}')
						(x,y) = self.input_move()
				if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
							file.write(F'Player {self.player_turn} under AI control plays: {chr(x + 65)}{y}\n')
							file.write(F'i   Evaluation time: {round(end - start, 7)}s\n')
							file.write(F'ii  Heuristic evaluations:{self.visited}\n')
							file.write(F'iii Evaluations by depth:\n')
							file.write(F'iv  Average evaluation depth:\n')
							file.write(F'v   Average recursion depth:\n')
							print(F'Player {self.player_turn} under AI control plays: {chr(x + 65)}{y}')
							print(F'Evaluation time: {round(end - start, 7)}s')
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
	
	def e1(self):
		boardArray = np.array(self.board.current_state)
		diags = [boardArray[::-1,:].diagonal(i) for i in range(-boardArray.shape[0]+1,boardArray.shape[1])]
		diags.extend(boardArray.diagonal(i) for i in range(boardArray.shape[1]-1,-boardArray.shape[0],-1))

		diagResult = list()
		for diag in diags:
			if len(diag) >= self.board.winning_size:
				diagResult.append(self.e1_logic(diag.tolist()))
				print(f'diagResult: {diagResult}')
		
		verticalResult = list()
		for i in range(0, self.board.board_size):
			print(self.board.current_state[i])
			verticalResult.append(self.e1_logic(self.board.current_state[i]))
			print(f'verticalResult: {verticalResult}')
		
		horizontalResult = list()
		for i in range(0, self.board.board_size):
			horizontalResult.append(self.e1_logic([row[i] for row in self.board.current_state]))
			print(f'horizontal: {horizontalResult}')

		return np.sum(diagResult) + np.sum(horizontalResult) + np.sum(verticalResult)
			
	def e1_logic(self, array):
		OCount = 1
		XCount = 1
		resultCount = 0
		for i in range(len(array)-1):
			if ((array[i] == array[i+1] or array[i+1] == '.' or array[i] == '.') and (array[i] == 'O' or array[i+1] == 'O')):
				XCount = 1
				OCount += 1
				if (OCount == self.board.winning_size):
					resultCount -= 1
			elif ((array[i] == array[i+1] or array[i+1] == '.' or array[i] == '.') and (array[i] == 'X' or array[i+1] == 'X')):
				OCount = 1
				XCount += 1
				if (XCount == self.board.winning_size):
					resultCount += 1
			elif (array[i] == array[i+1] and array[i] == '.'):
				XCount += 1
				OCount += 1
				if (XCount == self.board.winning_size):
					resultCount += 1
				if (OCount == self.board.winning_size):
					resultCount -= 1
			else:
				XCount = 1
				OCount = 1
		
		return resultCount

	def e2(self):
		boardArray = np.array(self.board.current_state)
		diags = [boardArray[::-1,:].diagonal(i) for i in range(-boardArray.shape[0]+1,boardArray.shape[1])]
		diags.extend(boardArray.diagonal(i) for i in range(boardArray.shape[1]-1,-boardArray.shape[0],-1))

		V = 0
		# Diagonal
		for diag in diags:
			for i in range(self.board.winning_size):
				if len(diag) >= self.board.winning_size:
					result = self.e2_logic(diag, self.board.winning_size - i)
					print(f'diag {result}')
					if result == 'X':
						V += 10**(self.board.winning_size - i)
						break
					elif result == 'O':
						V -= 10**(self.board.winning_size - i)
						break
		
		# Vertical
		for col in range(0, self.board.board_size):
			for i in range(self.board.winning_size):
				result = self.e2_logic(self.board.current_state[col], self.board.winning_size - i)
				print(f'col {result}')
				if result == 'X':
					V += 10**(self.board.winning_size - i)
					break
				elif result == 'O':
					V -= 10**(self.board.winning_size - i)
					break
		
		# Horizontal
		for rowIndex in range(0, self.board.board_size):
			for i in range(self.board.winning_size):
				result = self.e2_logic([row[rowIndex] for row in self.board.current_state], self.board.winning_size - i)
				print(f'rowIndex {result}')
				if result == 'X':
					V += 10**(self.board.winning_size - i)
					break
				elif result == 'O':
					V -= 10**(self.board.winning_size - i)
					break
		
		return V

	def e2_logic(self, array, streakSize):
		count = 1
		for i in range(len(array)-1):
			if (not(array[i] == '.' or array[i] == '*') and (streakSize == 1 or array[i] == array[i+1])):
				count += 1
				if (count == streakSize):
					return array[i]
			else:
				count = 1
		return None

