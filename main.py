I = 1
J = 2
L = 3
O = 4
S = 5
T = 6
Z = 7

NONE = 0
BLOCK = 1

DAS_LEFT = 1
DAS_RIGHT = 2
TAP_LEFT = 3
TAP_RIGHT = 4
ROTATE_LEFT = 5
ROTATE_RIGHT = 6
SOFT_DROP = 7
HARD_DROP = 8

SURFACES = {
	1: [[[0, 0, 0, 0]],
		[[0], [0], [0], [0]]],
	2: [[[0, 0], [0, 0], [0, 0]],
		[[0, 0, 0], [1, 1, 0]],
		[[0, 0], [0, 1], [0, 1]],
		[[0, 0, 0], [0, 0, 0]]],
	3: [[[0, 0], [0, 0], [0, 0]],
		[[0, 0, 0], [0, 1, 1]],
		[[0, 0], [1, 0], [1, 0]],
		[[0, 0, 0], [0, 0, 0]]],
	4: [[[0, 0], [0, 0]]],
	5: [[[0, 0, 0], [0, 0, 1]],
		[[0, 0], [0, 0], [1, 0]]],
	6: [[[0, 0, 0], [0, 0, 0]],
		[[0, 0], [0, 0], [0, 1]],
		[[0, 0, 0], [1, 0, 1]],
		[[0, 0], [0, 0], [1, 0]]],
	7: [[[0, 0, 0], [1, 0, 0]],
		[[0, 0], [0, 0], [0, 1]]],
}

IMAGES = {
	1: [[[0, 0, 0, 0]],
		[[0], [0], [0], [0]]],
	2: [[[1, 0], [1, 0], [0, 0]],
		[[0, 0, 0], [1, 1, 0]],
		[[0, 0], [0, 1], [0, 1]],
		[[0, 1, 1], [0, 0, 0]]],
	3: [[[0, 1], [0, 1], [0, 0]],
		[[0, 0, 0], [0, 1, 1]],
		[[0, 0], [1, 0], [1, 0]],
		[[1, 1, 0], [0, 0, 0]]],
	4: [[[0, 0], [0, 0]]],
	5: [[[1, 0, 0], [0, 0, 1]],
		[[0, 1], [0, 0], [1, 0]]],
	6: [[[1, 0, 1], [0, 0, 0]],
		[[0, 1], [0, 0], [0, 1]],
		[[0, 0, 0], [1, 0, 1]],
		[[1, 0], [0, 0], [1, 0]]],
	7: [[[0, 0, 1], [1, 0, 0]],
		[[1, 0], [0, 0], [0, 1]]],
}

MOVE_NAMES = {
	DAS_LEFT: "DAS_LEFT",
	DAS_RIGHT: "DAS_RIGHT",
	TAP_LEFT: "TAP_LEFT",
	TAP_RIGHT: "TAP_RIGHT",
	ROTATE_LEFT: "ROTATE_LEFT",
	ROTATE_RIGHT: "ROTATE_RIGHT",
	SOFT_DROP: "SOFT_DROP",
	HARD_DROP: "HARD_DROP",
}

PIECE_NAMES = {
	1: "I",
	2: "J",
	3: "L",
	4: "O",
	5: "S",
	6: "T",
	7: "Z",
}

class Bot:
	def __init__(self, queue):
		self.board = [[NONE] * 10 for _ in range(20)]
		self.queue = queue

	def format_board(self):
		# Formats the board onto a pretty string
		final = ""

		for row in self.board:
			final += "".join(["  " if col == NONE else "##" for col in row]) + "\n"

		return final

	def format_moves(self, moves):
		return [MOVE_NAMES[move] for move in moves]

	def format_pieces(self, pieces):
		return [PIECE_NAMES[piece] for piece in pieces]

	def find_top_rows(self, board=None):
		board = board or self.board

		# Board is divided in three layers, from top to bottom:
		# - Empty rows
		# - Stack top
		# - Stack body
		# This function finds the rows in the second layer
		bot = None
		top = 20

		# Search for top row
		for y, row in enumerate(board):
			# Isn't empty row
			if row != [NONE] * 10:
				top = y - 1
				break

		# Search for bottom row
		for y, row in enumerate(board[::-1]):
			y = 21 - y
			# Isn't stack body
			if row != [BLOCK] * 9 + [NONE]:
				bot = y
				break

		return (bot, top)

	def can_conveniently_place(self, piece, board=None):
		board = board or self.board

		surfaces = SURFACES[piece]

		for surface in surfaces:
			surface.append([BLOCK] * len(surface[0]))

		for y, row in enumerate(board[::-1]):
			y = 19 - y
			for x, col in enumerate(row):
				for i, surface in enumerate(surfaces):
					#print(f"Testing surface {i} at {x}, {y}")

					try:
						for sy, srow in enumerate(surface):
							for sx, scol in enumerate(srow):
								try:
									if not scol == board[y + sy][x + sx]:
										#print(f"  Surface cell at {sx}, {sy} doesn't match with {x}, {y}, stopping")
										raise StopIteration
								except IndexError:
									#print(f"  Cell {x+sx}, {y+sy} is out of bounds, stopping")
									raise StopIteration

						return (i, x, y)
					except StopIteration:
						pass

		return False

	def image_piece(self, x, y, piece, surface):
		image = IMAGES[piece][surface]

		for iy, irow in enumerate(image):
			for ix, icol in enumerate(irow):
				if icol == 0:
					self.board[y + iy][x + ix] = BLOCK

if __name__ == "__main__":
	import time, random

	bot = Bot(J)
	bot.board[17][3] = BLOCK
	bot.board[18][3] = BLOCK
	bot.board[18][1] = BLOCK
	bot.board[18][7] = BLOCK
	bot.board[19] = [BLOCK] * 9 + [NONE]
	#print(bot.format_board())
	#print(bot.find_top_rows())
	#rows = bot.find_top_rows()
	#print(bot.board[rows[1]:rows[0]])
	result = True
	queue = [J, T, O, J, I, L, S, Z]
	while result:
		current = queue.pop()
		result = bot.can_conveniently_place(current)
		print(result)
		if len(queue) == 0:
			queue = [J, T, O, J, I, L, S, Z]
			random.shuffle(queue)
		print(f"NEXT: {bot.format_pieces(queue)[-1]}")
		if result:
			i, x, y = result
			bot.image_piece(x, y, current, i)
			print(bot.format_board())
			time.sleep(1)
