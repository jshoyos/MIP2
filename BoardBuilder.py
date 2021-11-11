from Board import Board

class BoardBuilder:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.board_size = None
        self.number_blocks = None
        self.winning_size = None
        self.block_coordinates = None
    
    def boardSize(self):
        invalid_size = True
        while (invalid_size):
            try:
                self.board_size = int(input('Enter the desired board size:'))
            except ValueError as e:
                print('input must be an integer. Try again')
                continue
            if (self.board_size < 3 |self.board_size > 10):
                print('Invalid board size!!! Size must be between 3 and 10')
                self.board_size = None
            else:
                invalid_size = False

    def winningSize(self):
        invalid_winning_size = True
        if (self.board_size == None):
            print('board size must be determined first!')
        else:
            while (invalid_winning_size):
                try:
                    self.winning_size = int(input('Enter the desired winning line-up size:'))
                except ValueError as e:
                    print('input must be an integer. Try again')
                    continue
                if (self.winning_size < 3 |self.winning_size > self.board_size):
                    print(F'Invalid winning line-up size!!! Size must be between 3 and {self.board_size}')
                    self.winning_size = None
                else:
                    invalid_winning_size = False

    def blocks(self):
        invalide_block_size = True
        if (self.board_size == None):
            print('board size must be determined first!')
        else:
            while (invalide_block_size):
                try:
                    self.number_blocks = int(input('Enter the desired number of blocks:'))
                except ValueError as e:
                    print('input must be an integer. Try again')
                    continue
                if (self.number_blocks < 0 |self.number_blocks > 2*self.board_size):
                    print(F'Invalid number of blocks!!! Number of blocks must be between 0 and {2*self.board_size}')
                    self.number_blocks = None
                else:
                    invalide_block_size = False

    def coordinates(self):
        if (self.number_blocks == None):
            print('board size must be determined first!')
        else:
            self.block_coordinates = list(tuple())
            for i in range(0, self.number_blocks):
                invalid_coordinates = True
                while invalid_coordinates:
                    try:
                        x = int(input(f'Enter the x value for block #{i+1}:'))
                        y = int(input(f'Enter the y value for block #{i+1}:'))
                    except ValueError as e:
                        print('Coordinates must only contain integers!! Try again')
                    if not(x < self.board_size | x > self.board_size | y < self.board_size | y > self.board_size):
                        if ((x,y) in self.block_coordinates):
                            print('These coordiantes already contain a block')
                            i -= 1
                            continue
                        else:
                            self.block_coordinates.append((x,y))
                            invalid_coordinates = False

    def build(self):
        should_throw = False
        if (self.board_size == None):
            print('You must first determine a board size')
            should_throw = True
        else:
            if (self.winning_size == None):
                print('You must determine a winning length streak')
                should_throw = True
            if (self.number_blocks == None):
                print('You must first determine a number of blocks')
                should_throw = True
            else:
                if (self.block_coordinates == None):
                    print('You must determine the coordinates of the blocks')
                    should_throw = True
                elif (len(self.block_coordinates) != self.number_blocks):
                    print('All coordinates should be entered')
                    should_throw = True
        if (should_throw):
            raise Exception('Can\'t create board!')
        return Board(self.board_size, self.number_blocks, self.winning_size, self.block_coordinates)