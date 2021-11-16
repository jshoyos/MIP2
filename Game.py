import time

from numpy.lib.function_base import average
from Board import Board
from BoardBuilder import BoardBuilder
import numpy as np
import sys
from threading import Event, Timer

class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3

	def __init__(self, recommend = True):
		self.initialize_game()
		self.recommend = recommend 
		self.depth_array ={}
		self.depth_array_overall ={}
		self.ards = list()
		# self.count = 0
		self.avg_depth = 0
		self.stop_event = Event()
		self.visited = 0
		self.avg_time = []
		self.totalHeuristic = 0

	def initialize_game(self):
		self.board = BoardBuilder().boardSize().blocks().coordinates().winningSize().build()
		self.d1 = int(input('Enter the max depth for player one: '))
		self.d2 = int(input('Enter the max depth for player two: '))
		self.t = float(input('Enter the maximum time per turn: '))
		# Player X always plays first
		self.player_turn = 'X'
		self.move = 0

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
		print(f'(move #{self.move})')
		print(f' +', end="")
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
		file.write(f'\t(move #{self.move})')
		file.write(f'\n +')
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

	def check_end(self, file):
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
				self.timer.cancel()
				file.write('The winner is X!\n')
			elif self.result == 'O':
				print('The winner is O!')
				self.timer.cancel()
				file.write('The winner is O!\n')
			elif self.result == '.':
				print("It's a tie!")
				self.timer.cancel()
				file.write("It's a tie!\n")
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

	def minimax(self, max=False, depth = 0):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = sys.maxsize
		if max:
			value = -sys.maxsize - 1
		x = None
		y = None
		result = self.is_end()

		if result == 'X':
			return (-(sys.maxsize - 1)/2, x, y, depth)
		elif result == 'O':
			return (sys.maxsize/2, x, y,depth)
		elif result == '.':
			return (0, x, y, depth)
		elif self.stop_event.is_set():
			if self.player_turn == 'X':
				return (-(sys.maxsize - 1)/2, x, y,depth)
			else:
				return (sys.maxsize/2, x, y,depth)
		elif (self.player_turn == 'X' and self.d1 == depth) or (self.player_turn == 'O' and self.d2 == depth):
			if depth in self.depth_array_overall:
				self.depth_array_overall[depth] += 1
			else:
				self.depth_array_overall[depth] = 1
			
			if depth in self.depth_array:
				self.depth_array[depth] += 1
			else:
				self.depth_array[depth] = 1
			# self.count += 1
			if self.player_turn == 'X':
				return (self.e1(), x, y, depth)
			else:
				return (self.e2(), x, y, depth)
		ARD = []
		for i in range(0, self.board.board_size):
			for j in range(0, self.board.board_size):
				if self.board.current_state[i][j] == '.':
					if max:
						self.board.current_state[i][j] = 'O'
						(v, a, b, ard) = self.minimax(max=False, depth=depth+1)
						
						ARD.append(ard)
						if depth in self.depth_array_overall:
							self.depth_array_overall[depth] += 1
						else:
							self.depth_array_overall[depth] = 1
						if depth in self.depth_array:
							self.depth_array[depth] += 1
						else:
							self.depth_array[depth] = 1
						# self.count += 1
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.board.current_state[i][j] = 'X'
						(v, a, b, ard) = self.minimax(max=True,depth=depth+1)
						ARD.append(ard)
						if depth in self.depth_array_overall:
							self.depth_array_overall[depth] += 1
						else:
							self.depth_array_overall[depth] = 1
						if depth in self.depth_array:
							self.depth_array[depth] += 1
						else:
							self.depth_array[depth] = 1
						# self.count += 1
						if v < value:
							value = v
							x = i
							y = j
					self.board.current_state[i][j] = '.'
		return (value, x, y, round(np.average(np.asarray(ARD)), 2))

	def alphabeta(self,alpha=(-sys.maxsize - 1), beta=sys.maxsize, max=False, depth = 0):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = sys.maxsize
		if max:
			value = -sys.maxsize - 1
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-(sys.maxsize - 1)/2, x, y, depth)
		elif result == 'O':
			return (sys.maxsize/2, x, y, depth)
		elif result == '.':
			return (0, x, y, depth)
		elif self.stop_event.is_set():
			if self.player_turn == 'X':
				return (-(sys.maxsize - 1)/2, x, y, depth)
			else:
				return (sys.maxsize/2, x, y, depth)
		elif (self.player_turn == 'X' and self.d1 == depth) or (self.player_turn == 'O' and self.d2 == depth):
			if depth in self.depth_array_overall:
				self.depth_array_overall[depth] += 1
			else:
				self.depth_array_overall[depth] = 1
			if depth in self.depth_array:
				self.depth_array[depth] += 1
			else:
				self.depth_array[depth] = 1
			# self.count += 1
			if self.player_turn == 'X':
				return (self.e1(), x, y, depth)
			else:
				return (self.e2(), x, y, depth)
		ARD = list()
		for i in range(0, self.board.board_size):
			for j in range(0, self.board.board_size):
				if self.board.current_state[i][j] == '.':
					if max:
						self.board.current_state[i][j] = 'O'
						(v, a, b,ard) = self.alphabeta(alpha, beta, max=False, depth = depth + 1)
						ARD.append(ard)
						if depth in self.depth_array_overall:
							self.depth_array_overall[depth] += 1
						else:
							self.depth_array_overall[depth] = 1
						if depth in self.depth_array:
							self.depth_array[depth] += 1
						else:
							self.depth_array[depth] = 1
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.board.current_state[i][j] = 'X'
						(v, a, b, ard) = self.alphabeta(alpha, beta, max=True, depth = depth + 1)
						ARD.append(ard)
						if depth in self.depth_array_overall:
							self.depth_array_overall[depth] += 1
						else:
							self.depth_array_overall[depth] = 1
						if depth in self.depth_array:
							self.depth_array[depth] += 1
						else:
							self.depth_array[depth] = 1
						# self.count += 1
						if v < value:
							value = v
							x = i
							y = j
					self.board.current_state[i][j] = '.'
					if max: 
						if value >= beta:
							return (value, x, y, depth)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y, depth)
						if value < beta:
							beta = value
		return (value, x, y, round(np.average(np.asarray(ARD)), 2))

	def play(self,algo=None,player_x=None,player_o=None):
		n = self.board.board_size
		b = self.board.number_blocks
		s = self.board.winning_size
		t = self.t
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
				if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
					self.timer = Timer(self.t - 0.1, self.stopTurn, [file])
					self.timer.start()
				
				# self.count = 0
				self.avg_depth = 0
				self.visited = 0
				self.depth_array.clear()
				self.draw_board()
				self.draw_board_file(file)
				print('Going Again')
				if self.check_end(file):
					file.write(F'6(b)i   Average evaluation time: {np.average(np.asarray(self.avg_time))}s\n')
					file.write(F'6(b)ii  Total heuristic evaluations: {self.totalHeuristic}\n')
					file.write(F'6(b)iii Evaluations by depth: {self.depth_array_overall}\n')
					av_depth_total = 0.0
					for k in self.depth_array_overall.keys():
						av_depth_total += k* self.depth_array_overall[k]
					av_depth_total = av_depth_total/self.totalHeuristic
					file.write(F'6(b)iv  Average evaluation depth: {av_depth_total}\n')
					file.write(F'6(b)v   Average recursion depth:{np.average(np.asarray(self.ards))}\n')
					file.write(F'6(b)vi  Total moves: {self.move}\n')
					return
				start = time.time()
				if algo == self.MINIMAX:
					if self.player_turn == 'X':
						(_, x, y, ard) = self.minimax(max=False,)
					else:
						(_, x, y, ard) = self.minimax(max=True)
				else: # algo == self.ALPHABETA
					if self.player_turn == 'X':
						(_, x, y, ard) = self.alphabeta(max=False)
					else:
						(_, x, y, ard) = self.alphabeta(max=True)
				end = time.time()
				if self.stop_event.is_set():
					ard = 0
				self.ards.append(ard)
				self.avg_time.append(round(end - start, 7))
				if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
						if self.recommend:
							file.write(F'Evaluation time: {round(end - start, 7)}s')
							file.write(F'\nRecommended move: x = {chr(x+65)}, y = {y}')
							print(F'Evaluation time: {round(end - start, 7)}s')
							print(F'Recommended move: x = {chr(x+65)}, y = {y}')
						(x,y) = self.input_move()
				if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
							file.write(F'Player {self.player_turn} under AI control plays: {chr(x + 65)}{y}\n')
							file.write(F'i   Evaluation time: {round(end - start, 7)}s\n')
							for k in self.depth_array.keys():
								self.visited += self.depth_array[k]
							file.write(F'ii  Heuristic evaluations:{self.visited}\n')
							self.totalHeuristic += self.visited
							file.write(F'iii Evaluations by depth:{self.depth_array}\n')
							for k in self.depth_array.keys():
								self.avg_depth += k* self.depth_array[k]
							self.avg_depth = self.avg_depth/self.visited
							file.write(F'iv  Average evaluation depth:{round(self.avg_depth,1)}\n')
							file.write(F'v   Average recursion depth: {ard}\n')
							print(F'Player {self.player_turn} under AI control plays: {chr(x + 65)}{y}')
							print(F'Evaluation time: {round(end - start, 7)}s')
				self.board.current_state[x][y] = self.player_turn
				if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
					self.timer.cancel()
					self.stop_event.clear()
				self.move += 1	
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
	
	def e2(self):
		boardArray = np.array(self.board.current_state)
		diags = [boardArray[::-1,:].diagonal(i) for i in range(-boardArray.shape[0]+1,boardArray.shape[1])]
		diags.extend(boardArray.diagonal(i) for i in range(boardArray.shape[1]-1,-boardArray.shape[0],-1))

		diagResult = list()
		for diag in diags:
			if len(diag) >= self.board.winning_size:
				diagResult.append(self.e1_logic(diag.tolist()))
		
		verticalResult = list()
		for i in range(0, self.board.board_size):
			verticalResult.append(self.e1_logic(self.board.current_state[i]))
		
		horizontalResult = list()
		for i in range(0, self.board.board_size):
			horizontalResult.append(self.e1_logic([row[i] for row in self.board.current_state]))

		return np.sum(diagResult) + np.sum(horizontalResult) + np.sum(verticalResult)
			
	def e2_logic(self, array):
		""" Count number of possible plays leading to a possible win """
		""" We count the one for the max (player x) minus the one for min (player O) """
		OCount = 1
		XCount = 1
		resultCount = 0
		for i in range(len(array)-1):
			if ((array[i] == array[i+1] or array[i+1] == '.' or array[i] == '.') and (array[i] == 'O' or array[i+1] == 'O')):
				XCount = 1
				OCount -= 1
				if (OCount == self.board.winning_size):
					resultCount += 1
			elif ((array[i] == array[i+1] or array[i+1] == '.' or array[i] == '.') and (array[i] == 'X' or array[i+1] == 'X')):
				OCount = 1
				XCount -= 1
				if (XCount == self.board.winning_size):
					resultCount -= 1
			elif (array[i] == array[i+1] and array[i] == '.'):
				XCount -= 1
				OCount -= 1
				if (XCount == self.board.winning_size):
					resultCount -= 1
				if (OCount == self.board.winning_size):
					resultCount += 1
			else:
				XCount = 1
				OCount = 1
		
		return resultCount

	def e1(self):
		boardArray = np.array(self.board.current_state)
		diags = [boardArray[::-1,:].diagonal(i) for i in range(-boardArray.shape[0]+1,boardArray.shape[1])]
		diags.extend(boardArray.diagonal(i) for i in range(boardArray.shape[1]-1,-boardArray.shape[0],-1))

		result = list()
		# Diagonal
		for diag in diags:
			if len(diag) >= self.board.winning_size:
				result.append(self.e2_logic(diag))
		
		# Vertical
		for col in range(self.board.board_size):
			column = np.asarray(self.board.current_state[col])
			result.append(self.e2_logic(column))
		
		# Horizontal
		for rowIndex in range(0, self.board.board_size):
			currentRow = np.asarray([row[rowIndex] for row in self.board.current_state])
			result.append(self.e2_logic(currentRow))
		return np.sum(result)

	def e1_logic(self, array):
		XCount = np.count_nonzero(array == 'X')
		OCount = np.count_nonzero(array == 'O')
		return OCount - XCount
	
	def stopTurn(self, file):
		print('*** Out of time play now ***')
		file.write('*** Out of time play now ***\n')
		self.stop_event.set()