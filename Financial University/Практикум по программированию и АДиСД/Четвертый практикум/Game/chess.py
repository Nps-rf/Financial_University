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

    @classmethod
    def run(cls) -> None:
        """
        The main function for launching the application
        :return: pygame application
        """
        while cls._running:
            cls.__prepare()
            Sound.init()
            Graphics.board_graphics()
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
        drawings = Controls.settings()
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
        cls.__look4click()

    @classmethod
    def __console(cls, available=False, coordinate=False) -> None:
        if available:
            print('\033[1m\033[32mSquares you can move -> ', *cls.available, end='\n\033[0m')
        if coordinate:
            print(f'\033[1m\033[34mx = {cls.column}, y = {cls.row}', end='\n\033[0m')

    @classmethod
    def __return_move(cls, pos) -> None:
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
        if cls.piece[0][1] == 'K':
            return True
        return False

    @classmethod
    def __is_knight(cls) -> bool:
        return cls.piece[0][1] == 'N'

    @classmethod
    def _update_history_(cls) -> None:
        cls.history.append([[cls.piece[1][1], cls.piece[1][0]],  # from
                            [cls.column, cls.row],  # to
                            cls.piece[0],  # who moves
                            Table.field[cls.row][cls.column],  # from-old
                            cls.current_player.letter,  # Who moved
                            'beat' if Table.field[cls.row][cls.column][0] == cls.current_player.opposite
                            else 'move'])  # move status

    @classmethod
    def _piece_chose_(cls) -> None:
        if Table.field[cls.row][cls.column] != '--' \
                and Table.field[cls.row][cls.column][0] != cls.current_player.opposite:
            cls.chosen = True
            coordinates = [cls.y, cls.x] = cls.row, cls.column
            cls.piece = (Table.field[cls.row][cls.column], coordinates)

    @classmethod
    def _call_sg_(cls) -> None:
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
        Table.field[cls.row][cls.column] = cls.piece[0]
        Table.field[cls.piece[1][0]][cls.piece[1][1]] = '--'

    @classmethod
    def switch_player(cls) -> None:
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
        Checks whether the user clicked on the cross (or other place)
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
        for move in Rules.side_available(player, opposite_side=True, all_allowed=True, only_beat=True):
            while move in moves:
                del moves[moves.index(move)]

    @classmethod
    def _init_mate_(cls) -> None:
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
        b2 = Graphics.button_list[1]
        if b2.rect.collidepoint(pos):
            Chess.show_menu = True
            cls.settings(run_only=True)

    @classmethod
    def settings(cls, run_only=False) -> (Menu, Buttons):
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
        [b1, b2, b0] = cls.settings()[1:]
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
    Class responsible of pieces moving rules
    """
    @staticmethod
    def pawn(p_x, p_y, *_, only_beat=False, all_allowed=False) -> Available_moves:
        """
        :param all_allowed:
        :param only_beat:
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        # Movement section
        available = []
        beat = []
        all_way = []
        if not only_beat:
            try:
                if Table.field[p_y + 1][p_x] == '--':
                    if p_y == 1 and Table.field[p_y][p_x][0] != 'w' and p_y + 1 < 8:
                        available.append([p_x, p_y + 2]) if Table.field[p_y + 2][p_x] == '--' else None
                        available.append([p_x, p_y + 1])
                    elif Table.field[p_y][p_x][0] == 'b' and p_y + 1 < 8:
                        available.append([p_x, p_y + 1])
            except IndexError:
                pass
            try:
                if Table.field[p_y - 1][p_x] == '--':
                    if p_y == 6 and Table.field[p_y][p_x][0] != 'b' and p_y - 1 >= 0:
                        available.append([p_x, p_y - 1])
                        available.append([p_x, p_y - 2]) if Table.field[p_y - 2][p_x] == '--' else None
                    elif Table.field[p_y][p_x][0] == 'w' and p_y - 1 >= 0:
                        available.append([p_x, p_y - 1])
            except IndexError:
                pass
        # White Beat section
        if Table.field[p_y][p_x][0] == 'w':
            try:
                if all_allowed and not Rules.under_attack(p_x - 1, p_y - 1):
                    all_way.append([p_x - 1, p_y - 1])
                if Table.field[p_y - 1][p_x - 1][0] == 'b' or only_beat:
                    available.append([p_x - 1, p_y - 1])
                if only_beat:
                    beat.append([p_x - 1, p_y - 1])
            except IndexError:
                pass

            try:
                if all_allowed and not Rules.under_attack(p_x + 1, p_y - 1):
                    all_way.append([p_x + 1, p_y - 1])
                if Table.field[p_y - 1][p_x + 1][0] == 'b' or only_beat:
                    available.append([p_x + 1, p_y - 1])
                if only_beat:
                    beat.append([p_x + 1, p_y - 1])
            except IndexError:
                pass

        # Black Beat section
        if Table.field[p_y][p_x][0] == 'b':
            try:
                if all_allowed and not Rules.under_attack(p_x - 1, p_y + 1):
                    all_way.append([p_x - 1, p_y + 1])
                if Table.field[p_y + 1][p_x - 1][0] == 'w' or only_beat:
                    available.append([p_x - 1, p_y + 1])
                if only_beat:
                    beat.append([p_x - 1, p_y + 1])
            except IndexError:
                pass

            try:
                if all_allowed and not Rules.under_attack(p_x + 1, p_y + 1):
                    all_way.append([p_x + 1, p_y + 1])
                if Table.field[p_y + 1][p_x + 1][0] == 'w' or only_beat:
                    available.append([p_x + 1, p_y + 1])
                if only_beat:
                    beat.append([p_x + 1, p_y + 1])
            except IndexError:
                pass
        if all_allowed:
            return all_way
        return available if not only_beat else beat

    @staticmethod
    def knight(p_x, p_y, player, only_beat=False, all_allowed=False) -> Available_moves:
        """
        :param all_allowed:
        :param only_beat:
        :param player:
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        table = Table.field
        available = []
        beat = []
        all_way = []

        # leftward
        try:
            if all_allowed:
                all_way.append([p_x - 2, p_y - 1])
            if table[p_y - 1][p_x - 2][0] != player.letter and (p_x - 2 >= 0 and p_y - 1 >= 0):
                available.append([p_x - 2, p_y - 1])
                if table[p_y - 1][p_x - 2][0] == player.opposite and table[p_y - 1][p_x - 2][1] == 'K':
                    beat.append([p_x - 2, p_y - 1])
        except IndexError:
            pass
        try:
            if all_allowed:
                all_way.append([p_x - 2, p_y + 1])
            if table[p_y + 1][p_x - 2][0] != player.letter and (p_x - 2 >= 0 and p_y + 1 < 8):
                available.append([p_x - 2, p_y + 1])
                if table[p_y + 1][p_x - 2][0] == player.opposite and table[p_y + 1][p_x - 2][1] == 'K':
                    beat.append([p_x - 2, p_y + 1])
        except IndexError:
            pass
        # above
        try:
            if all_allowed:
                all_way.append([p_x - 1, p_y - 2])
            if table[p_y - 2][p_x - 1][0] != player.letter and (p_x - 1 >= 0 and p_y - 2 >= 0):
                available.append([p_x - 1, p_y - 2])
                if table[p_y - 2][p_x - 1][0] == player.opposite and table[p_y - 2][p_x - 1][1] == 'K':
                    beat.append([p_x - 1, p_y - 2])
        except IndexError:
            pass
        try:
            if all_allowed:
                all_way.append([p_x + 1, p_y - 2])
            if table[p_y - 2][p_x + 1][0] != player.letter and (p_x + 1 < 8 and p_y - 2 >= 0):
                available.append([p_x + 1, p_y - 2])
                if table[p_y - 2][p_x + 1][0] == player.opposite and table[p_y - 2][p_x + 1][1] == 'K':
                    beat.append([p_x + 1, p_y - 2])
        except IndexError:
            pass

        # on the right
        try:
            if all_allowed:
                all_way.append([p_x + 2, p_y - 1])
            if table[p_y - 1][p_x + 2][0] != player.letter and (p_x + 2 < 8 and p_y - 1 >= 0):
                available.append([p_x + 2, p_y - 1])
                if table[p_y - 1][p_x + 2][0] == player.opposite and table[p_y - 1][p_x + 2][1] == 'K':
                    beat.append([p_x + 2, p_y - 1])
        except IndexError:
            pass
        try:
            if all_allowed:
                all_way.append([p_x + 2, p_y + 1])
            if table[p_y + 1][p_x + 2][0] != player.letter and (p_x + 2 < 8 and p_y + 1 < 8):
                available.append([p_x + 2, p_y + 1])
                if table[p_y + 1][p_x + 2][0] == player.opposite and table[p_y + 1][p_x + 2][1] == 'K':
                    beat.append([p_x + 2, p_y + 1])
        except IndexError:
            pass
        # below
        try:
            if all_allowed:
                all_way.append([p_x - 1, p_y + 2])
            if table[p_y + 2][p_x - 1][0] != player.letter and (p_x - 1 >= 0 and p_y + 2 < 8):
                available.append([p_x - 1, p_y + 2])
                if table[p_y + 2][p_x - 1][0] == player.opposite and table[p_y + 2][p_x - 1][1] == 'K':
                    beat.append([p_x - 1, p_y + 2])
        except IndexError:
            pass
        try:
            if all_allowed:
                all_way.append([p_x + 1, p_y + 2])
            if table[p_y + 2][p_x + 1][0] != player.letter and (p_x + 1 < 8 and p_y + 2 < 8):
                available.append([p_x + 1, p_y + 2])
                if table[p_y + 2][p_x + 1][0] == player.opposite and table[p_y + 2][p_x + 1][1] == 'K':
                    beat.append([p_x + 1, p_y + 2])
        except IndexError:
            pass
        if all_allowed:
            return all_way
        return available if not only_beat else beat

    @staticmethod
    def bishop(p_x, p_y, player, only_beat=False, all_allowed=False) -> Available_moves:
        """
        :param all_allowed:
        :param only_beat:
        :param player:
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        available = []
        beat = []
        all_way = []

        def solve_side(beat, upper=True, left=True, all_allowed=False) -> Available_moves:
            local_all_allowed = all_allowed
            no_way = False
            a_local = []
            for x, y in zip(range(1, 8 + 1), range(1, 8 + 1)):
                if not upper:
                    y = -y
                if not left:
                    x = -x
                if no_way:
                    break
                if 0 <= p_x - x < 8 and 0 <= p_y - y < 8:
                    try:
                        if local_all_allowed:
                            if Rules.under_attack(p_x - x, p_y - y) \
                                    and Table.field[p_y - y][p_x - x][0] != player.opposite:
                                local_all_allowed = False
                            all_way.append([p_x - x, p_y - y])
                        if Table.field[p_y - y][p_x - x][0] == player.opposite and not all_allowed:
                            available.append([p_x - x, p_y - y])
                            a_local.append([p_x - x, p_y - y])
                            no_way = True
                            if only_beat and Table.field[p_y - y][p_x - x][1] == 'K':
                                beat += a_local
                            break
                        if Table.field[p_y - y][p_x - x][0] != player.letter:
                            available.append([p_x - x, p_y - y])
                            a_local.append([p_x - x, p_y - y])
                        elif Table.field[p_y - y][p_x - x][0] == player.letter:
                            no_way = True
                            break
                    except IndexError:
                        pass
        # upper left
        solve_side(beat=beat, all_allowed=all_allowed)

        # lower left
        solve_side(upper=False, beat=beat, all_allowed=all_allowed)

        # upper right
        solve_side(left=False, beat=beat, all_allowed=all_allowed)

        # lower right
        solve_side(left=False, upper=False, beat=beat, all_allowed=all_allowed)

        if all_allowed:
            return all_way
        return available if not only_beat else beat

    @staticmethod
    def rook(p_x, p_y, player, only_beat=False, all_allowed=False) -> Available_moves:
        """
        :param all_allowed:
        :param only_beat:
        :param player:
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        available = []
        beat = []
        all_way = []

        def solve_side(beat, vertical=False, invert=False, all_allowed=False) -> None:
            local_all_allowed = all_allowed
            no_way = False
            a_local = []
            for x in range(1, 8):
                y = x if vertical else 0
                x = 0 if vertical else x
                x = -x if invert else x
                y = -y if invert else y
                if no_way:
                    break
                if 0 <= p_x - x < 8 and 0 <= p_y - y < 8:
                    try:
                        if local_all_allowed:
                            if Rules.under_attack(p_x - x, p_y - y)\
                                    and Table.field[p_y - y][p_x - x][0] != player.opposite:
                                local_all_allowed = False
                            all_way.append([p_x - x, p_y - y])
                        if Table.field[p_y - y][p_x - x][0] == player.letter:
                            no_way = True
                            break
                        if Table.field[p_y - y][p_x - x][0] == player.opposite and not all_allowed:
                            available.append([p_x - x, p_y - y])
                            a_local.append([p_x - x, p_y - y])
                            no_way = True
                            if Table.field[p_y - y][p_x - x][1] == 'K':
                                beat += a_local
                            break
                        if Table.field[p_y - y][p_x - x][0] != player.letter:
                            available.append([p_x - x, p_y - y])
                            a_local.append([p_x - x, p_y - y])
                    except IndexError:
                        pass

        solve_side(beat=beat, all_allowed=all_allowed)
        solve_side(invert=True, beat=beat, all_allowed=all_allowed)
        solve_side(vertical=True, beat=beat, all_allowed=all_allowed)
        solve_side(vertical=True, invert=True, beat=beat, all_allowed=all_allowed)

        if all_allowed:
            return all_way
        return available if not only_beat else beat

    @staticmethod
    def queen(p_x, p_y, player, only_beat=False, all_allowed=False) -> Available_moves:
        """
        :param all_allowed:
        :param only_beat:
        :param player:
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        beat = []
        all_way = []
        available = Rules.rook(p_x, p_y, player)
        if only_beat:
            beat = Rules.rook(p_x, p_y, player, only_beat=only_beat)
        if all_allowed:
            all_way = Rules.rook(p_x, p_y, player, all_allowed=all_allowed)
        available += Rules.bishop(p_x, p_y, player)
        if only_beat:
            beat += Rules.bishop(p_x, p_y, player, only_beat=only_beat)
        if all_allowed:
            all_way += Rules.bishop(p_x, p_y, player, all_allowed=all_allowed)
        if all_allowed:
            return all_way
        return available if not only_beat else beat

    @staticmethod
    def king(p_x, p_y, player, only_beat=False, all_allowed=False) -> Available_moves:
        """
        :param all_allowed:
        :param only_beat:
        :param player:
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        available = []
        beat = []
        all_way = []
        try:
            if all_allowed:
                all_way.append([p_x, p_y - 1])
            if Table.field[p_y - 1][p_x][0] != player.letter and (0 <= p_y - 1 < 8 and 0 <= p_x < 8):
                available.append([p_x, p_y - 1])
                if only_beat and Table.field[p_y - 1][p_x][1] == 'K' and (0 <= p_y - 1 < 8 and 0 <= p_x < 8):
                    beat.append([p_x, p_y - 1])

        except IndexError:
            pass
        try:
            if all_allowed:
                all_way.append([p_x, p_y + 1])
            if Table.field[p_y + 1][p_x][0] != player.letter and (0 <= p_y + 1 < 8 and 0 <= p_x < 8):
                available.append([p_x, p_y + 1])
                if only_beat and Table.field[p_y + 1][p_x][1] == 'K' and (0 <= p_y + 1 < 8 and 0 <= p_x < 8):
                    beat.append([p_x, p_y + 1])
        except IndexError:
            pass
        try:
            if all_allowed:
                all_way.append([p_x - 1, p_y])
            if Table.field[p_y][p_x - 1][0] != player.letter and (0 <= p_y < 8 and 0 <= p_x - 1 < 8):
                available.append([p_x - 1, p_y])
                if only_beat and Table.field[p_y][p_x - 1][1] == 'K' and (0 <= p_y < 8 and 0 <= p_x - 1 < 8):
                    beat.append([p_x - 1, p_y])
        except IndexError:
            pass
        try:
            if all_allowed:
                all_way.append([p_x + 1, p_y])
            if Table.field[p_y][p_x + 1][0] != player.letter and (0 <= p_y < 8 and 0 <= p_x + 1 < 8):
                available.append([p_x + 1, p_y])
                if only_beat and Table.field[p_y][p_x + 1][1] == 'K' and (0 <= p_y < 8 and 0 <= p_x + 1 < 8):
                    beat.append([p_x + 1, p_y])
        except IndexError:
            pass
        try:
            if all_allowed:
                all_way.append([p_x - 1, p_y - 1])
            if Table.field[p_y - 1][p_x - 1][0] != player.letter and (0 <= p_y - 1 < 8 and 0 <= p_x - 1 < 8):
                available.append([p_x - 1, p_y - 1])
                if only_beat and Table.field[p_y - 1][p_x - 1][1] == 'K' and (0 <= p_y - 1 < 8 and 0 <= p_x - 1 < 8):
                    beat.append([p_x - 1, p_y - 1])
        except IndexError:
            pass
        try:
            if all_allowed:
                all_way.append([p_x + 1, p_y - 1])
            if Table.field[p_y - 1][p_x + 1][0] != player.letter and (0 <= p_y - 1 < 8 and 0 <= p_x + 1 < 8):
                available.append([p_x + 1, p_y - 1])
                if only_beat and Table.field[p_y - 1][p_x + 1][1] == 'K' and (0 <= p_y - 1 < 8 and 0 <= p_x + 1 < 8):
                    beat.append([p_x + 1, p_y - 1])
        except IndexError:
            pass
        try:
            if all_allowed:
                all_way.append([p_x + 1, p_y + 1])
            if Table.field[p_y + 1][p_x + 1][0] != player.letter and (0 <= p_y + 1 < 8 and 0 <= p_x + 1 < 8):
                available.append([p_x + 1, p_y + 1])
                if only_beat and Table.field[p_y + 1][p_x + 1][1] == 'K' and (0 <= p_y + 1 < 8 and 0 <= p_x + 1 < 8):
                    beat.append([p_x + 1, p_y + 1])
        except IndexError:
            pass
        try:
            if all_allowed:
                all_way.append([p_x - 1, p_y + 1])
            if Table.field[p_y + 1][p_x - 1][0] != player.letter and (0 <= p_y + 1 < 8 and 0 <= p_x - 1 < 8):
                available.append([p_x - 1, p_y + 1])
                if only_beat and Table.field[p_y + 1][p_x - 1][1] == 'K' and (0 <= p_y + 1 < 8 and 0 <= p_x - 1 < 8):
                    beat.append([p_x - 1, p_y + 1])
        except IndexError:
            pass
        if all_allowed:
            return all_way
        return available if not only_beat else beat

    @staticmethod
    def side_available(player, opposite_side=False, only_beat=False, all_allowed=False) -> Available_moves:
        movements = Controls.movements
        side_available = []
        if opposite_side:
            Controls.switch_player()
            player = Controls.current_player
        for x in range(8):
            for y in range(8):
                if Table.field[y][x][0] == player.letter:
                    if Table.field[y][x][1] == 'p':
                        side_available.extend(movements[Table.field[y][x][1]](x, y, player, only_beat=only_beat))
                    elif all_allowed:
                        side_available.extend(movements[Table.field[y][x][1]](x, y, player, all_allowed=all_allowed))
                    else:
                        side_available.extend(movements[Table.field[y][x][1]](x, y, player))
        if opposite_side:
            Controls.switch_player()
        return side_available

    @staticmethod
    def basic_check(p_x, p_y, player) -> Available_moves:
        available = []
        for turn in Controls.movements[Table.field[p_y][p_x][1]](p_x, p_y, player):
            available.append(Table.field[turn[1]][turn[0]])
        return available

    @staticmethod
    def __find_king(side='w'):
        for x in range(8):
            for y in range(8):
                if Table.field[y][x] == f'{side}K':
                    return [x, y]

    @staticmethod
    def under_attack(x, y):
        piece = Table.field[y][x]
        player = Controls.current_player
        color = piece[0]
        switched = False
        if color == 'w':
            if piece == '--':
                return False
            if player.letter == 'w':
                switched = True
                Controls.switch_player()
            player = Controls.current_player
            available = Rules.side_available(player=player)
            if switched:
                Controls.switch_player()
            return [x, y] in available
        else:
            if piece == '--':
                return False
            if player.letter == 'b':
                switched = True
                Controls.switch_player()
            player = Controls.current_player
            available = Rules.side_available(player=player)
            if switched:
                Controls.switch_player()
            return [x, y] in available

    @staticmethod
    def __can_escape(moves):
        Flag = True
        for move in moves:
            if Rules.under_attack(move[0], move[1]):
                Flag = False
            else:
                Flag = True
                break
        if len(moves) > 0:
            return Flag
        else:
            return False

    @staticmethod
    def naive_mate(enemy, player) -> bool:
        # I must find exact way, which allows enemy beat king
        Controls.switch_player()
        player_king = Controls.current_player
        king_pos = Rules.__find_king(player_king.letter)
        Controls.available = Controls.movements['K'](king_pos[0], king_pos[1], player_king)
        Controls.prevent_wrong_move(Controls.available, player_king)
        Controls.switch_player()
        beat_way = set(map(tuple, Controls.movements[Table.field[enemy[0]][enemy[1]][1]](enemy[1], enemy[0], player,
                                                                                         only_beat=True)))
        side_available = set(map(tuple, Rules.side_available(player, opposite_side=True)))

        return (enemy[::-1] not in side_available and beat_way.isdisjoint(side_available)
                and len(Controls.available) == 0) or \
               (enemy[::-1] not in side_available and not Rules.__can_escape(Controls.available))


if __name__ == '__main__':
    CHESS_GAME = Chess
    CHESS_GAME.run()
