import pygame
from Misc.__types__ import *
from Misc.Button import Button
from Misc.Text import Text
from itertools import cycle
from Board import Table
from Misc.Build import Build
from SoundSystem import Sound
from Player import Player


class Chess:
	"""
	Creates an application
	Abbreviations scheme:
	◈ First letter -> color of piece
	◈ Second letter -> exact piece
	Example:
		◈ wK -> White King
	Pieces:
		◈ K -> King (Король)
		◈ Q -> Queen (Ферзь)
		◈ R -> Rook (Ладья)
		◈ B -> Bishop (Слон)
		◈ N -> Knight (Конь)
		◈ P -> Pawn (Пешка)
	"""
	__instance = None

	_running = True
	_responce = True
	show_menu = False

	def __new__(cls, *args, **kwargs):
		if cls.__instance is None:
			cls.__instance = super().__new__(cls)

		return cls.__instance

	@classmethod
	def __del__(cls):
		cls.__instance = None

	@classmethod
	def __prepare(cls) -> None:
		"""
		Function that prepares an application for launch
		"""
		pygame.mixer.pre_init(44100, -16, 1, 512)
		pygame.init()
		Graphics.init()
		Sound.init()
		Graphics.board_graphics()

	@classmethod
	def run(cls) -> None:
		"""
		The main function for launching the application
		:return: pygame application
		"""
		while cls._running:
			cls.__prepare()
			Graphics.print_info()
			Graphics.turn_owner()
			for b in Graphics.get_button_list():
				Graphics.draw_button(b)
			if not cls.show_menu:
				Controls.run_controls()
			else:
				Controls.___maintenance_of_settings__()
			if cls.show_menu:
				Graphics.draw_menu()

			pygame.display.update()


class Graphics:
	"""
	The class responsible for the graphical component of the application
	"""
	__pos = None
	__output = pygame.font.Font.render
	__output_error = 670
	__expand = 12  # The error for the screen resolution (so that the figures do not move out)
	__DIMENSIONS = 8

	_font = pygame.font.Font
	_images = Build.load_images()
	_screen = pygame.display

	resolution = (WIDTH, HEIGHT) = (720, 720)
	SQUARE_SIZE = WIDTH // __DIMENSIONS
	available_moves = list()
	button_list = list()
	strings = []
	show_moves = True

	@classmethod
	def __getattribute__(cls, item):
		if item == 'SQUARE_SIZE':
			raise ValueError('Access denied')
		else:
			return object.__getattribute__(cls, item)

	@classmethod
	def init(cls):
		cls._screen = pygame.display.set_mode((cls.resolution[0] + (cls.resolution[0] // 3 + 50),
											   cls.resolution[1]))
		cls._screen.fill('white')
		pygame.draw.rect(
			cls._screen,
			pygame.Color('dark grey'),
			pygame.Rect(
				5,  # Horizontal coordinate
				0,  # Vertical coordinate
				cls.resolution[0],  # Size of square
				cls.resolution[0])  # Size of square
		)
		cls._font = pygame.font.Font(None, 24)
		pygame.display.set_caption('Chess')

	@classmethod
	def get_button_list(cls) -> Buttons:
		cancel: Callable[[], None] = lambda: print('Turn canceled')
		settings: Callable[[], None] = lambda: print('Settings opened')
		button1 = Button((867, 45), (250, 50), (220, 220, 220), (255, 0, 0), cancel, 'Отменить ход')
		button2 = Button((867, 675), (250, 50), (220, 220, 220), (255, 0, 0), settings, 'Настройки')

		cls.button_list.append(button1)
		cls.button_list.append(button2)
		return cls.button_list

	@classmethod
	def draw_button(cls, b):
		b.draw(cls._screen)

	@classmethod
	def draw_menu(cls):
		drawings = Controls.initialize_settings()
		cls._screen.blit(drawings[0], (-75, 0))
		drawings[1].draw(cls._screen)
		drawings[2].draw(cls._screen)
		drawings[3].draw(cls._screen)

	@classmethod
	def board_graphics(cls):  # whole process in couple
		"""
		The main function for creating board and putting a pieces and showing available moves
		"""
		cls._board_()
		cls._pieces_()
		if len(cls.available_moves) > 0 and cls.show_moves:
			cls.show_available_moves()

	@classmethod
	def _board_(cls) -> None:
		colors = [pygame.Color('white'), pygame.Color('dark gray')]
		for row in range(cls.__DIMENSIONS):
			for col in range(cls.__DIMENSIONS):
				color = colors[((row + col) % 2)]  # Implementation Color Switching
				pygame.draw.rect(
					cls._screen,
					color,
					pygame.Rect(
						col * cls.SQUARE_SIZE,  # Horizontal coordinate
						row * cls.SQUARE_SIZE,  # Vertical coordinate
						cls.SQUARE_SIZE,  # Size of square
						cls.SQUARE_SIZE)  # Size of square
				)

	@classmethod
	def _pieces_(cls) -> None:
		"""
		Put a pieces on board
		"""
		board = Table.field
		for row in range(cls.__DIMENSIONS):
			for col in range(cls.__DIMENSIONS):
				piece = board[row][col]
				if piece != '--':  # if not empty square
					cls._screen.blit(
						cls._images[piece],  # Picture of piece
						pygame.Rect(
							col * cls.SQUARE_SIZE + cls.__expand,  # Horizontal coordinate
							row * cls.SQUARE_SIZE + cls.__expand,  # Vertical coordinate
							cls.SQUARE_SIZE,  # Size of square
							cls.SQUARE_SIZE)  # Size of square
					)

	@classmethod
	def turn_owner(cls):
		# noinspection PyArgumentList
		text = cls._font.render(Controls.current_player.name, 1, pygame.Color('purple'))
		pos = text.get_rect(center=(cls.resolution[0] + 140, cls.resolution[1] - 706))
		cls._screen.blit(text, pos)

	@classmethod
	def show_available_moves(cls) -> None:
		color = (32, 64, 128, 128)
		available_move = pygame.Surface((cls.resolution[0], cls.resolution[0]), pygame.SRCALPHA)
		pygame.draw.rect(
			available_move,  # Square
			color,
			pygame.Rect(
				cls.available_moves[0][0] * cls.SQUARE_SIZE,  # Horizontal coordinate
				cls.available_moves[0][1] * cls.SQUARE_SIZE,  # Vertical coordinate
				cls.SQUARE_SIZE,  # Size of square
				cls.SQUARE_SIZE)  # Size of square
		)
		cls._screen.blit(available_move, dest=(0, 0))
		for square in cls.available_moves[1::]:
			color = (0, 150, 0, 120) if Table.field[square[1]][square[0]] == '--' else (150, 0, 0, 120)
			available_move = pygame.Surface((cls.resolution[0], cls.resolution[0]), pygame.SRCALPHA)
			pygame.draw.rect(
				available_move,  # Square
				color,
				pygame.Rect(
					square[0] * cls.SQUARE_SIZE,  # Horizontal coordinate
					square[1] * cls.SQUARE_SIZE,  # Vertical coordinate
					cls.SQUARE_SIZE,  # Size of square
					cls.SQUARE_SIZE)  # Size of square
			)
			cls._screen.blit(available_move, dest=(0, 0))

	# noinspection PyArgumentList
	@staticmethod
	def info_gainer(piece) -> Action_Info:
		pieces = {
			'K': 'Король',
			'Q': 'Ферзь',
			'R': 'Ладья',
			'B': 'Слон',
			'N': 'Конь',
			'p': 'Пешка'
		}
		string = f'{pieces[piece[1]]} {"белых" if piece[0] == "w" else "черных"}' \
				 f' {"повержена" if piece[1] == "p" or piece[1] == "R" else "повержен"}!'
		return string

	@classmethod
	def print_info(cls):
		error = cls.__output_error
		for string in cls.strings:
			error -= 35
			# noinspection PyArgumentList
			cls.__output = cls._font.render(string, 1, pygame.Color('red'))
			cls.__pos = cls.__output.get_rect(center=(cls.resolution[0] + 140, cls.resolution[1] - error))
			cls._screen.blit(cls.__output, cls.__pos)

	@classmethod
	def check_pos(cls, event):
		x = (event.pos[0] // (cls.resolution[0] // cls.__DIMENSIONS)) > 7
		y = event.pos[1] // (cls.resolution[0] // cls.__DIMENSIONS) > 7
		return x | y

	@classmethod
	def get_square(cls, event) -> tuple:
		column = event.pos[0] // (cls.resolution[0] // cls.__DIMENSIONS)
		row = event.pos[1] // (cls.resolution[0] // cls.__DIMENSIONS)
		return column, row


class Controls:
	__responce = True

	WHITE = Player()
	BLACK = Player(letter='b', opposite='w', name='Black')
	_statement_gen_1, _statement_gen_2 = cycle({'Включить', 'Выключить'}), cycle({'Включить', 'Выключить'})
	available = list()
	history = list()
	row, column = None, None
	current_player = WHITE
	chosen = False
	piece = ('--', [-1, -1])
	x, y = None, None
	muted = False
	snd_statement, moves_statement = 'Выключить', 'Выключить'
	movements = dict()

	@classmethod
	def run_controls(cls) -> None:
		"""
		:return: None
		Easy-run of controls system
		"""
		cls.__look4click()

	@classmethod
	def __console(cls, available=False, coordinate=False) -> None:
		"""
		:param available:
		:param coordinate:
		:return: None
		Helpful console output with useful information about:
			1) Available squares for chosen piece
			2) Your current position
		"""
		if available:
			print('\033[1m\033[32mSquares you can move -> ', *cls.available, end='\n\033[0m')
		if coordinate:
			print(f'\033[1m\033[34mx = {cls.column}, y = {cls.row}', end='\n\033[0m')

	@classmethod
	def __return_move(cls, pos) -> None:
		"""
		:param pos:
		:return: None
		Method responsible of cancelling last move, when we click cancel-move-button
		"""
		b1 = Graphics.button_list[0]
		if b1.rect.collidepoint(pos):
			for number, turn in enumerate(cls.history[::-1]):
				x_return = turn[0][0]
				y_return = turn[0][1]
				Table.field[y_return][x_return] = turn[2]
				Table.field[turn[1][1]][turn[1][0]] = turn[3]
				Sound.play_sound(name='move', muted=cls.muted)

				cls.current_player = cls.BLACK if turn[4] == 'b' else cls.WHITE
				cls.chosen = True
				Graphics.available_moves.clear()
				cls.available.clear()
				cls.x, cls.y = None, None
				del cls.history[-1]

				if turn[5] == 'beat':
					del Graphics.strings[-1]

				if 'check' in turn:
					del Graphics.strings[-1]

				break

	@classmethod
	def __is_king(cls) -> bool:
		"""
		:return: bool
		:rtype: bool
		"""
		if cls.piece[0][1] == 'K':
			return True
		return False

	@classmethod
	def __is_knight(cls) -> bool:
		"""
		:return: bool
		:rtype: bool
		"""
		return cls.piece[0][1] == 'N'

	@classmethod
	def _update_history_(cls) -> None:
		"""
		:return: None
		Update all available history.
		Useful for debug :)
		"""
		cls.history.append([[cls.piece[1][1], cls.piece[1][0]],  # from
							[cls.column, cls.row],  # to
							cls.piece[0],  # who moves
							Table.field[cls.row][cls.column],  # from-old
							cls.current_player.letter,  # Who moved
							'beat' if Table.field[cls.row][cls.column][0] == cls.current_player.opposite
							else 'move'])  # move status

	@classmethod
	def _piece_chose_(cls) -> None:
		"""
		:return: None
		Responsible for piece-chose
		"""
		if Table.field[cls.row][cls.column] != '--' \
				and Table.field[cls.row][cls.column][0] != cls.current_player.opposite:
			cls.chosen = True
			coordinates = [cls.y, cls.x] = cls.row, cls.column
			cls.piece = (Table.field[cls.row][cls.column], coordinates)

	@classmethod
	def _call_sg_(cls) -> None:
		"""
		:return: None
		sg -> Sound&Graphics
		Responsible for running Sound and Graphics maintenance
		"""
		if cls.x is not None or cls.y is not None:
			cls.available = cls.movements[cls.piece[0][1]](cls.x, cls.y, cls.current_player)
			if cls.__is_king():
				cls.prevent_wrong_move(cls.available, cls.current_player)

			if Table.field[cls.row][cls.column][0] != cls.current_player.opposite \
					and Table.field[cls.row][cls.column] != '--':
				if len(Graphics.available_moves) > 0:
					Graphics.available_moves.clear()
				Sound.play_sound(name=Table.field[cls.row][cls.column][1], muted=cls.muted)  # playing sound
				Graphics.available_moves.append([cls.x, cls.y])
				Graphics.available_moves += cls.available  # show available moves

	@classmethod
	def _move_piece_(cls) -> None:
		"""
		:return: None
		Used for moving a piece
		"""
		Table.field[cls.row][cls.column] = cls.piece[0]
		Table.field[cls.piece[1][0]][cls.piece[1][1]] = '--'

	@classmethod
	def switch_player(cls) -> None:
		"""
		:return: None
		Method for switching current player
		"""
		cls.current_player = cls.BLACK if cls.current_player.letter == 'w' else cls.WHITE

	@classmethod
	def _is_available_(cls) -> bool:
		return [cls.column, cls.row] in cls.available and cls.current_player.letter == cls.piece[0][0]

	@classmethod
	def _is_beat_(cls) -> bool:
		return Table.field[cls.row][cls.column][0] == cls.current_player.opposite

	@classmethod
	def _is_move_(cls) -> bool:
		return Table.field[cls.row][cls.column] == '--'

	@classmethod
	def __look4click(cls) -> None:
		"""
		Checks whether the user clicked on the cross or other place
		Just a heart of user interaction
		"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Chess._running = False

			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and cls.__responce:
				# move return section section
				pos = pygame.mouse.get_pos()
				cls.__return_move(pos=pos)
				cls._call_settings(pos=pos)
				if event.pos is None:
					return None
				# move&beat section
				if Graphics.check_pos(event):
					break
				else:
					cls.column, cls.row = Graphics.get_square(event)
				cls.movements = {
					'p': Rules.pawn,
					'N': Rules.knight,
					'B': Rules.bishop,
					'R': Rules.rook,
					'Q': Rules.queen,
					'K': Rules.king
				}

				# get coordinates and misc
				cls._piece_chose_()
				# play sound of chosen piece and look for all squares available to move
				cls._call_sg_()  # SG -> Sound&Graphics

				if cls.chosen:  # figure chosen and can move
					if cls.__is_king():  # is piece a king
						# check for king and remove unavailable moves
						cls.prevent_wrong_move(cls.available, cls.current_player)
					cls.__console(available=True)
					# movement of piece
					if cls._is_available_():
						if cls._is_beat_():  # if you beat piece
							Sound.play_sound(name='beat', muted=cls.muted)
							Graphics.strings.append(Graphics.info_gainer(Table.field[cls.row][cls.column]))
						elif cls.__is_knight():  # Knight move sound
							Sound.play_sound(name='Knight_move', muted=cls.muted)
						elif cls._is_move_():  # Classic move sound
							Sound.play_sound(name='move', muted=cls.muted)
						cls._update_history_()
						cls._move_piece_()
						cls._init_mate_()
						cls.chosen = False
						cls.switch_player()
						Graphics.available_moves.clear()

					cls.__console(coordinate=True)

	@staticmethod
	def prevent_wrong_move(moves, player) -> None:
		"""
		:param moves:
		:param player:
		:return: None
		Used for preventing king's wrong move.
		"""
		for move in Rules.side_available(player, opposite_side=True):
			while move in moves:
				del moves[moves.index(move)]

	@classmethod
	def _init_mate_(cls) -> None:
		"""
		:return: None
		Runs mate procedure with graphics and sound
		"""
		for move in Rules.basic_check(cls.column, cls.row, cls.current_player):
			if move == 'wK':
				if Rules.naive_mate((cls.row, cls.column), cls.current_player):
					Graphics.strings.append('Шах и мат белым!')
					Sound.play_sound(name='checkmate', muted=cls.muted)
					cls.__responce = False
					Graphics.button_list.append(
						Text(
							msg='Шах и мат белым!',
							position=(Graphics.resolution[0] // 2 - 222, Graphics.resolution[0] // 2 - 75),
							clr=(255, 0, 0),
							font_size=64)
					)
				else:
					Graphics.strings.append('Шах белым!')
					Sound.play_sound(name='check', muted=cls.muted)
					cls.history[-1].append('check')
			elif move == 'bK':
				if Rules.naive_mate((cls.row, cls.column), cls.current_player):
					Graphics.strings.append('Шах и мат черным!')
					Sound.play_sound(name='checkmate', muted=cls.muted)
					cls.__responce = False
					Graphics.button_list.append(
						Text(
							msg='Шах и мат черным!',
							position=(Graphics.resolution[0] // 2 - 222, Graphics.resolution[0] // 2 - 75),
							clr=(255, 0, 0),
							font_size=64)
					)
				else:
					Graphics.strings.append('Шах черным!')
					Sound.play_sound(name='check', muted=cls.muted)
					cls.history[-1].append('check')

	@classmethod
	def _call_settings(cls, pos) -> None:
		"""
		:param pos:
		:return: None
		Used for calling settings
		"""
		b2 = Graphics.button_list[1]
		if b2.rect.collidepoint(pos):
			Chess.show_menu = True
			cls.initialize_settings(run_only=True)

	@classmethod
	def initialize_settings(cls, run_only=False) -> (Menu, Buttons):
		"""
		:param run_only:
		:return: (Menu, Buttons)
		Create buttons and switch their state
		"""
		if not run_only:
			if cls.muted:
				cls.snd_statement = 'Включить'
			else:
				cls.snd_statement = 'Выключить'
			if not Graphics.show_moves:
				cls.moves_statement = 'Включить'
			else:
				cls.moves_statement = 'Выключить'
			menu = pygame.image.load('Stock/menu.jpg')
			button0 = Button((520, 185), (250, 50), (128, 220, 55), (128, 25, 64), text='Вернуться обратно')
			button1 = Button((520, 255), (250, 50), (128, 220, 220), (128, 255, 255),
							 text=f'{cls.moves_statement} подсветку ходов')
			button2 = Button((520, 325), (250, 50), (128, 220, 220), (128, 255, 255), text=f'{cls.snd_statement} звук')
			return menu, button1, button2, button0

	@classmethod
	def ___maintenance_of_settings__(cls) -> None:
		"""
		:return: None
		Heart of interaction with buttons
		"""
		[b1, b2, b0] = cls.initialize_settings()[1:]
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Chess._running = False

			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = pygame.mouse.get_pos()
				if b0.rect.collidepoint(pos):
					Chess.show_menu = False
				elif b2.rect.collidepoint(pos):
					cls.muted = not cls.muted
					cls.snd_statement = next(cls._statement_gen_1)
				elif b1.rect.collidepoint(pos):
					Graphics.show_moves = not Graphics.show_moves
					cls.moves_statement = next(cls._statement_gen_2)


class Rules:
	"""
	Class responsible for piece movement rules, refactored for clarity and reduced repetition.
	"""

	@staticmethod
	def in_bounds(x, y):
		return 0 <= x < 8 and 0 <= y < 8

	@staticmethod
	def pawn(p_x, p_y, *_, only_beat=False, all_allowed=False) -> Available_moves:
		board = Table.field
		piece = board[p_y][p_x]
		color = piece[0]
		available, beat, all_way = [], [], []

		def try_append(x, y, arr):
			if Rules.in_bounds(x, y):
				arr.append([x, y])

		direction = -1 if color == 'w' else 1
		start_row = 6 if color == 'w' else 1

		if not only_beat:
			forward_one = (p_x, p_y + direction)
			if Rules.in_bounds(*forward_one) and board[forward_one[1]][forward_one[0]] == '--':
				available.append([forward_one[0], forward_one[1]])

				if p_y == start_row:
					forward_two = (p_x, p_y + 2 * direction)
					if Rules.in_bounds(*forward_two) and board[forward_two[1]][forward_two[0]] == '--':
						available.append([forward_two[0], forward_two[1]])

		# Pawn captures diagonally
		left_diag = (p_x - 1, p_y + direction)
		right_diag = (p_x + 1, p_y + direction)

		def handle_beat(dx, dy):
			if Rules.in_bounds(dx, dy):
				target = board[dy][dx]
				enemy_color = 'b' if color == 'w' else 'w'
				# Mark attacked squares if all_allowed is True
				if all_allowed:
					all_way.append([dx, dy])
				# If there is an enemy piece (including the king) on the diagonal, pawn can capture it
				if target != '--' and target[0] == enemy_color:
					available.append([dx, dy])
					if only_beat:
						beat.append([dx, dy])

		handle_beat(*left_diag)
		handle_beat(*right_diag)

		if all_allowed:
			return all_way
		return available if not only_beat else beat

	@staticmethod
	def knight(p_x, p_y, player, all_allowed=False) -> Available_moves:
		board = Table.field
		moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
		available, all_way = [], []

		for dx, dy in moves:
			nx, ny = p_x + dx, p_y + dy
			if Rules.in_bounds(nx, ny):
				if all_allowed:
					all_way.append([nx, ny])
				if board[ny][nx][0] != player.letter:
					available.append([nx, ny])

		return all_way if all_allowed else available

	@staticmethod
	def bishop(p_x, p_y, player, all_allowed=False) -> Available_moves:
		directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
		return Rules._slide_moves(p_x, p_y, player, directions, all_allowed)

	@staticmethod
	def rook(p_x, p_y, player, all_allowed=False) -> Available_moves:
		directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		return Rules._slide_moves(p_x, p_y, player, directions, all_allowed)

	@staticmethod
	def queen(p_x, p_y, player, all_allowed=False) -> Available_moves:
		# Queen = Rook + Bishop
		rook_moves = Rules.rook(p_x, p_y, player, all_allowed)
		bishop_moves = Rules.bishop(p_x, p_y, player, all_allowed)
		return rook_moves + bishop_moves

	@staticmethod
	def king(p_x, p_y, player, all_allowed=False) -> Available_moves:
		board = Table.field
		moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (1, 1), (-1, 1)]
		available, all_way = [], []
		for dx, dy in moves:
			nx, ny = p_x + dx, p_y + dy
			if Rules.in_bounds(nx, ny):
				if all_allowed:
					all_way.append([nx, ny])
				if board[ny][nx][0] != player.letter:
					available.append([nx, ny])
		return all_way if all_allowed else available

	@staticmethod
	def _slide_moves(p_x, p_y, player, directions, all_allowed=False) -> Available_moves:
		"""
		Helper method for bishop, rook, and queen moves.
		"""
		board = Table.field
		available = []
		all_way = []
		for dx, dy in directions:
			steps = 1
			local_all_allowed = all_allowed
			while True:
				nx, ny = p_x + dx * steps, p_y + dy * steps
				if not Rules.in_bounds(nx, ny):
					break
				if local_all_allowed:
					all_way.append([nx, ny])

				target = board[ny][nx]
				if target[0] == player.letter:
					break
				else:
					available.append([nx, ny])
					if target != '--':
						break
				steps += 1
		return all_way if all_allowed else available

	@staticmethod
	def side_available(player, opposite_side=False) -> Available_moves:
		movements = Controls.movements
		board = Table.field
		side_avail = []

		if opposite_side:
			Controls.switch_player()
			player = Controls.current_player

		for x in range(8):
			for y in range(8):
				if board[y][x][0] == player.letter:
					piece_type = board[y][x][1]
					side_avail.extend(movements[piece_type](x, y, player))

		if opposite_side:
			Controls.switch_player()

		return side_avail

	@staticmethod
	def basic_check(p_x, p_y, player) -> Available_moves:
		piece = Table.field[p_y][p_x][1]
		moves = Controls.movements[piece](p_x, p_y, player)
		return [Table.field[m[1]][m[0]] for m in moves]

	@staticmethod
	def __find_king(side: str = 'w') -> list:
		for y in range(8):
			for x in range(8):
				if Table.field[y][x] == f'{side}K':
					return [x, y]

	@staticmethod
	def under_attack(x, y) -> bool:
		piece = Table.field[y][x]
		player = Controls.current_player
		if piece == '--':
			return False
		color = piece[0]

		switched = False
		if color == player.letter:
			switched = True
			Controls.switch_player()

		new_player = Controls.current_player
		# Get all allowed moves for the opposite side
		available = Rules.side_available(player=new_player)

		if switched:
			Controls.switch_player()

		return [x, y] in available

	@staticmethod
	def __can_escape(moves) -> bool:
		# Returns True if any move is not under attack
		return any(not Rules.under_attack(mx, my) for mx, my in moves)

	@staticmethod
	def naive_mate(enemy, player) -> bool:
		Controls.switch_player()
		player_king = Controls.current_player
		king_pos = Rules.__find_king(player_king.letter)
		Controls.available = Controls.movements['K'](king_pos[0], king_pos[1], player_king)
		Controls.prevent_wrong_move(Controls.available, player_king)
		Controls.switch_player()

		side_available = set(map(tuple, Rules.side_available(player, opposite_side=True)))
		no_escape = len(Controls.available) == 0 or not Rules.__can_escape(Controls.available)

		return enemy[::-1] not in side_available and no_escape


if __name__ == '__main__':
	CHESS_GAME = Chess
	CHESS_GAME.run()
