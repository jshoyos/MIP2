# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python
from Game import Game
def main():
	s = open("scoreboard.txt","a")
	g = Game(recommend=True)
	useMin = int(input('Press 1 to use a minimax, or press 0 to use alphabeta: '))
	playerOneType = int(input('Press 1 if player one is human, press 0 if player one is AI: '))
	playerTwoType = int(input('Press 1 if player two is human, press 0 if player two is AI: '))
	algo = Game.MINIMAX if useMin else Game.ALPHABETA
	playerOneType = Game.HUMAN if playerOneType else Game.AI
	playerTwoType = Game.HUMAN if playerTwoType else Game.AI
	g.play(algo=algo,player_x=playerOneType,player_o=playerTwoType)
	# g.test1()
	g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.AI)

	s.write("\n")
	s.write("10 games\n")
	
	s.write(F'Total wins for heuristic e1:\n')
	s.write(F'Total wins for heurisitc e2:\n')
	s.write("\n")

	s.write(F'i   Average evaluation time: {sum(Game.sb_avg_eval_times)/len(Game.sb_avg_eval_times)}\n')
	s.write(F'ii  Total heuristics evaluations:{sum(Game.sb_total_heuristic)/len(Game.sb_total_heuristic)}\n')
	s.write(F'iii Evaluations by depth:{Game.sb_eval_by_depth} \n')
	s.write(F'iv  Average evaluation depth:{sum(Game.sb_avg_eval_depth)/len(Game.sb_avg_eval_depth)} \n')
	s.write(F'v   Average recursion depth:{sum(Game.sb_avg_rec_depth)/len(Game.sb_avg_rec_depth)} \n')
	s.write(F'vi  Average moves per game:{sum(Game.sb_avg_moves)/len(Game.sb_avg_moves)} \n')


if __name__ == "__main__":
	main()