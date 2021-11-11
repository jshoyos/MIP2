class Board:
    def __init__(self, board_size, number_blocks, winning_size, block_coordinates) -> None:
        self.board_size = board_size
        self.number_blocks = number_blocks
        self.winning_size = winning_size
        self.current_state = [['.']* self.board_size for i in range(0, self.board_size)]
        for x, y in block_coordinates:
            self.current_state[x][y] = 'B'
