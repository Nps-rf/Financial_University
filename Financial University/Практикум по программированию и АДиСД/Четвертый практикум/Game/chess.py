from init import *


class Player:
    def __init__(self, letter='w', opposite='b', name='White'):
        # self.score = 0  TODO
        self.name = name
        self.letter = letter
        self.opposite = opposite


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
    pos = None
    screen = pygame.display
    font = pygame.font.Font
    images = Build.load_images()
    running = True
    responce = True
    WHITE = Player()
    BLACK = Player(letter='b', opposite='w', name='Black')
    output = pygame.font.Font.render
    resolution = (WIDTH, HEIGHT) = (720, 720)
    DIMENSIONS = 8
    SQUARE_SIZE = WIDTH // DIMENSIONS
    expand = 12  # The error for the screen resolution (so that the figures do not move out)
    show_menu = False

    @classmethod
    def _prepare_(cls):
        """
        Function that prepares an application for launch
        """
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        cls.screen = pygame.display.set_mode((cls.resolution[0] + (cls.resolution[0] // 3 + 50), cls.resolution[1]))
        cls.screen.fill('white')
        pygame.draw.rect(
            cls.screen,
            pygame.Color('dark grey'),
            pygame.Rect(
                5,  # Horizontal coordinate
                0,  # Vertical coordinate
                cls.resolution[0],  # Size of square
                cls.resolution[0])  # Size of square
        )
        cls.font = pygame.font.Font(None, 24)
        pygame.display.set_caption('Chess')

    @classmethod
    def run(cls):
        """
        The main function for launching the application
        :return: pygame application
        """
        while cls.running:
            cls._prepare_()
            Sound.init()
            Graphics.board_graphics()
            Graphics.print_info()
            for b in Graphics.get_button_list():
                b.draw(cls.screen)
            if not cls.show_menu:
                Controls.run_controls()
            else:
                Controls.maintenance_of_settings()
            if cls.show_menu:
                drawings = Controls.settings()
                cls.screen.blit(drawings[0], (-75, 0))
                drawings[1].draw(cls.screen)
                drawings[2].draw(cls.screen)
                drawings[3].draw(cls.screen)

            pygame.display.update()


class Graphics(Chess):
    """
    The class responsible for the graphical component of the application
    """
    available_moves = list()
    button_list = list()
    output_error = 670
    strings = []
    show_moves = True

    @classmethod
    def get_button_list(cls):
        cancel: Callable[[], None] = lambda: print('Turn canceled')
        settings: Callable[[], None] = lambda: print('Settings opened')
        button1 = Button((867, 45), (250, 50), (220, 220, 220), (255, 0, 0), cancel, 'Отменить ход')
        button2 = Button((867, 675), (250, 50), (220, 220, 220), (255, 0, 0), settings, 'Настройки')

        cls.button_list.append(button1)
        cls.button_list.append(button2)
        return cls.button_list

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
    def _board_(cls):
        colors = [pygame.Color('white'), pygame.Color('dark gray')]
        for row in range(cls.DIMENSIONS):
            for col in range(cls.DIMENSIONS):
                color = colors[((row + col) % 2)]  # Implementation Color Switching
                pygame.draw.rect(
                    super().screen,
                    color,
                    pygame.Rect(
                        col * cls.SQUARE_SIZE,  # Horizontal coordinate
                        row * cls.SQUARE_SIZE,  # Vertical coordinate
                        cls.SQUARE_SIZE,  # Size of square
                        cls.SQUARE_SIZE)  # Size of square
                                )

    @classmethod
    def _pieces_(cls):
        """
        Put a pieces on board
        """
        board = Table.field
        for row in range(cls.DIMENSIONS):
            for col in range(cls.DIMENSIONS):
                piece = board[row][col]
                if piece != '--':  # if not empty square
                    super().screen.blit(
                        cls.images[piece],  # Picture of piece
                        pygame.Rect(
                            col * cls.SQUARE_SIZE + super().expand,  # Horizontal coordinate
                            row * cls.SQUARE_SIZE + super().expand,  # Vertical coordinate
                            cls.SQUARE_SIZE,  # Size of square
                            cls.SQUARE_SIZE)  # Size of square
                                    )

    @classmethod
    def show_available_moves(cls):
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
        super().screen.blit(available_move, dest=(0, 0))
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
            super().screen.blit(available_move, dest=(0, 0))

    # noinspection PyArgumentList
    @staticmethod
    def info_gainer(piece):
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
        error = cls.output_error
        for string in cls.strings:
            error -= 35
            # noinspection PyArgumentList
            cls.output = cls.font.render(string, 1, pygame.Color('red'))
            cls.pos = cls.output.get_rect(center=(super().resolution[0] + 140, super().resolution[1] - error))
            cls.screen.blit(cls.output, cls.pos)


class Controls(Chess, Sound):
    _statement_gen_1 = cycle({'Включить', 'Выключить'})
    _statement_gen_2 = cycle({'Включить', 'Выключить'})
    available = list()
    history = []
    old_piece = '--'
    row = None
    column = None
    current_player = Chess.WHITE
    chose = False
    piece = ('--', [-1, -1])
    x = None
    y = None
    muted = False
    snd_statement = 'Выключить'
    moves_statement = 'Выключить'

    @classmethod
    def run_controls(cls):
        cls._look4click_()

    @classmethod
    def _return_move_(cls, pos):
        b1 = Graphics.button_list[0]
        if b1.rect.collidepoint(pos):
            for number, turn in enumerate(cls.history[::-1]):
                x_return = turn[0][0]
                y_return = turn[0][1]
                Table.field[y_return][x_return] = turn[2]
                Table.field[turn[1][1]][turn[1][0]] = turn[3]
                Sound.play_sound(name='move', muted=cls.muted)
                ########################################################################################
                cls.current_player = super().BLACK if turn[4] == 'b' else super().WHITE
                cls.chose = True
                Graphics.available_moves.clear()
                cls.available.clear()
                cls.x, cls.y = None, None
                del cls.history[-1]
                ########################################################################################
                if turn[5] == 'beat':
                    del Graphics.strings[-1]
                ########################################################################################
                if 'check' in turn:
                    del Graphics.strings[-1]
                ########################################################################################
                break

    @classmethod
    def _look4click_(cls):
        """
        Checks whether the user clicked on the cross (or other place)
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Chess.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and cls.responce and event.button == 1:
                # move return section section
                pos = pygame.mouse.get_pos()
                cls._return_move_(pos=pos)
                cls.call_settings(pos=pos)
                if event.pos is None:
                    return None
                # move&beat section
                if event.pos[0] // (cls.resolution[0] // cls.DIMENSIONS) > 7 or \
                        event.pos[1] // (cls.resolution[0] // cls.DIMENSIONS) > 7:
                    break
                else:
                    cls.column = event.pos[0] // (cls.resolution[0] // cls.DIMENSIONS)
                    cls.row = event.pos[1] // (cls.resolution[0] // cls.DIMENSIONS)
                movements = {
                    'p': Rules.pawn,
                    'N': Rules.knight,
                    'B': Rules.bishop,
                    'R': Rules.rook,
                    'Q': Rules.queen,
                    'K': Rules.king
                }

                # get coordinates and misc
                if Table.field[cls.row][cls.column] != '--' \
                        and Table.field[cls.row][cls.column][0] != cls.current_player.opposite:
                    cls.chose = True
                    coordinates = [cls.y, cls.x] = cls.row, cls.column
                    cls.piece = (Table.field[cls.row][cls.column], coordinates)

                # play sound of chosen piece and look for all squares available to move
                if cls.x or cls.y is not None:
                    cls.available = movements[cls.piece[0][1]](cls.x, cls.y, cls.current_player)
                    if cls.piece[0][1] == 'K':
                        cls.prevent_wrong_move(movements)

                    if Table.field[cls.row][cls.column][0] != cls.current_player.opposite \
                            and Table.field[cls.row][cls.column] != '--':
                        if len(Graphics.available_moves) > 0:
                            Graphics.available_moves.clear()
                        Sound.play_sound(name=Table.field[cls.row][cls.column][1], muted=cls.muted)  # playing sound
                        Graphics.available_moves.append([cls.x, cls.y])
                        Graphics.available_moves += cls.available  # show available moves

                    if cls.chose:  # figure chosen and can move
                        if cls.piece[0][1] == 'K':
                            # check for king and remove unavailable moves
                            cls.prevent_wrong_move(movements)
                        print('Squares you can move -> ', *cls.available)
                        # movement of piece
                        if [cls.column, cls.row] in cls.available \
                                and cls.current_player.letter == cls.piece[0][0]:

                            if Table.field[cls.row][cls.column][0] == cls.current_player.opposite:
                                Sound.play_sound(name='beat', muted=cls.muted)
                                Graphics.strings.append(Graphics.info_gainer(Table.field[cls.row][cls.column]))

                            elif cls.piece[0][1] == 'N':
                                Sound.play_sound(name='Knight_move', muted=cls.muted)

                            elif Table.field[cls.row][cls.column] == '--':
                                Sound.play_sound(name='move', muted=cls.muted)

                            cls.old_x_y = [cls.column, cls.row]

                            cls.old_piece = Table.field[cls.row][cls.column] \
                                if Table.field[cls.row][cls.column] == '--' else '--'

                            cls.history.append([[cls.piece[1][1], cls.piece[1][0]],  # from
                                                [cls.column, cls.row],  # to
                                                cls.piece[0],  # who moves
                                                Table.field[cls.row][cls.column],  # from-old
                                                cls.current_player.letter,  # Who moved
                                                'beat' if Table.field[cls.row][cls.column][0] ==
                                                cls.current_player.opposite else 'move'])  # move status

                            Table.field[cls.row][cls.column] = cls.piece[0]

                            Table.field[cls.piece[1][0]][cls.piece[1][1]] = cls.old_piece
                            ############################################################################################
                            cls._init_mate(movements)
                            ############################################################################################
                            cls.chose = False
                            cls.current_player = super().BLACK if cls.current_player.letter == 'w' else super().WHITE
                            Graphics.available_moves.clear()
                            ############################################################################################

                print(f'x = {cls.column}, y = {cls.row}')

    @classmethod
    def prevent_wrong_move(cls, movements):
        for move in Rules.side_available(movements, cls.current_player, opposite_side=True):
            while move in cls.available:
                del cls.available[cls.available.index(move)]

    @classmethod
    def _init_mate(cls, movements):
        for move in Rules.basic_check(cls.column, cls.row, movements, cls.current_player):
            if move == 'wK':
                if Rules.naive_mate(cls.available, movements, cls.current_player):
                    Graphics.strings.append('Шах и мат белым!')
                    Sound.play_sound(name='checkmate', muted=cls.muted)
                    cls.responce = False
                    Graphics.button_list.append(
                        Text(
                            msg='Шах и мат белым!',
                            position=(Chess.resolution[0] // 2 - 222, Chess.resolution[0] // 2 - 75),
                            clr=(255, 0, 0),
                            font_size=64)
                    )
                else:
                    Graphics.strings.append('Шах белым!')
                    Sound.play_sound(name='check', muted=cls.muted)
                    cls.history[-1].append('check')
            elif move == 'bK':
                if Rules.naive_mate(cls.available, movements, cls.current_player):
                    Graphics.strings.append('Шах и мат черным!')
                    Sound.play_sound(name='checkmate', muted=cls.muted)
                    cls.responce = False
                    Graphics.button_list.append(
                        Text(
                            msg='Шах и мат черным!',
                            position=(Chess.resolution[0] // 2 - 222, Chess.resolution[0] // 2 - 75),
                            clr=(255, 0, 0),
                            font_size=64)
                    )
                else:
                    Graphics.strings.append('Шах черным!')
                    Sound.play_sound(name='check', muted=cls.muted)
                    cls.history[-1].append('check')

    @classmethod
    def call_settings(cls, pos):
        b2 = Graphics.button_list[1]
        if b2.rect.collidepoint(pos):
            Chess.show_menu = True
            cls.settings(run_only=True)

    @classmethod
    def settings(cls, run_only=False):  # TODO
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
    def maintenance_of_settings(cls):
        [b1, b2, b0] = cls.settings()[1:]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Chess.running = False

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
    def pawn(p_x, p_y, *_, only_beat=False):
        """
        :param only_beat:
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        # Movement section
        available = []
        beat = []
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
                if Table.field[p_y - 1][p_x - 1][0] == 'b' or only_beat:
                    available.append([p_x - 1, p_y - 1])
            except IndexError:
                pass

            try:
                if Table.field[p_y - 1][p_x + 1][0] == 'b' or only_beat:
                    available.append([p_x + 1, p_y - 1])
            except IndexError:
                pass

        # Black Beat section
        if Table.field[p_y][p_x][0] == 'b':
            try:
                if Table.field[p_y + 1][p_x - 1][0] == 'w' or only_beat:
                    available.append([p_x - 1, p_y + 1])
                    beat.append([p_x - 1, p_y + 1])
            except IndexError:
                pass

            try:
                if Table.field[p_y + 1][p_x + 1][0] == 'w' or only_beat:
                    available.append([p_x + 1, p_y + 1])
            except IndexError:
                pass

        return available

    @staticmethod
    def knight(p_x, p_y, player, only_beat=False):
        """
        :param only_beat:
        :param player:
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        table = Table.field
        available = []
        beat = []

        # leftward
        try:
            if table[p_y - 1][p_x - 2][0] != player.letter and (p_x - 2 >= 0 and p_y - 1 >= 0):
                available.append([p_x - 2, p_y - 1])
                if table[p_y - 1][p_x - 2][0] == player.opposite:
                    beat.append([p_x - 2, p_y - 1])
        except IndexError:
            pass
        try:
            if table[p_y + 1][p_x - 2][0] != player.letter and (p_x - 2 >= 0 and p_y + 1 < 8):
                available.append([p_x - 2, p_y + 1])
        except IndexError:
            pass
        # above
        try:
            if table[p_y - 2][p_x - 1][0] != player.letter and (p_x - 1 >= 0 and p_y - 2 >= 0):
                available.append([p_x - 1, p_y - 2])
        except IndexError:
            pass
        try:
            if table[p_y - 2][p_x + 1][0] != player.letter and (p_x + 1 < 8 and p_y - 2 >= 0):
                available.append([p_x + 1, p_y - 2])
        except IndexError:
            pass

        # on the right
        try:
            if table[p_y - 1][p_x + 2][0] != player.letter and (p_x + 2 < 8 and p_y - 1 >= 0):
                available.append([p_x + 2, p_y - 1])
        except IndexError:
            pass
        try:
            if table[p_y + 1][p_x + 2][0] != player.letter and (p_x + 2 < 8 and p_y + 1 < 8):
                available.append([p_x + 2, p_y + 1])
        except IndexError:
            pass
        # below
        try:
            if table[p_y + 2][p_x - 1][0] != player.letter and (p_x - 1 >= 0 and p_y + 2 < 8):
                available.append([p_x - 1, p_y + 2])
        except IndexError:
            pass
        try:
            if table[p_y + 2][p_x + 1][0] != player.letter and (p_x + 1 < 8 and p_y + 2 < 8):
                available.append([p_x + 1, p_y + 2])
        except IndexError:
            pass
        return available

    @staticmethod
    def bishop(p_x, p_y, player, only_beat=False):
        """
        :param only_beat:
        :param player:
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        available = []
        beat = []

        def solve_side(upper=True, left=True):
            no_way = False
            for x, y in zip(range(1, 8 + 1), range(1, 8 + 1)):
                if not upper:
                    y = -y
                if not left:
                    x = -x
                if no_way:
                    break
                if 0 <= p_x - x < 8 and 0 <= p_y - y < 8:
                    try:
                        if Table.field[p_y - y][p_x - x][0] == player.opposite:
                            available.append([p_x - x, p_y - y])
                            no_way = True
                            break
                        if Table.field[p_y - y][p_x - x][0] != player.letter:
                            available.append([p_x - x, p_y - y])
                        elif Table.field[p_y - y][p_x - x][0] == player.letter:
                            no_way = True
                            break
                    except IndexError:
                        pass
        # upper left
        solve_side()

        # lower left
        solve_side(upper=False)

        # upper right
        solve_side(left=False)

        # lower right
        solve_side(left=False, upper=False)

        return available

    @staticmethod
    def rook(p_x, p_y, player, only_beat=False):
        """
        :param only_beat:
        :param player:
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        available = []
        beat = []

        def solve_side(vertical=False, invert=False):
            no_way = False
            for x in range(1, 8):
                y = x if vertical else 0
                x = 0 if vertical else x
                x = -x if invert else x
                y = -y if invert else y
                if no_way:
                    break
                if 0 <= p_x - x < 8 and 0 <= p_y - y < 8:
                    try:
                        if Table.field[p_y - y][p_x - x][0] == player.opposite:
                            available.append([p_x - x, p_y - y])
                            no_way = True
                            break
                        if Table.field[p_y - y][p_x - x][0] != player.letter:
                            available.append([p_x - x, p_y - y])
                        elif Table.field[p_y - y][p_x - x][0] == player.letter:
                            no_way = True
                            break
                    except IndexError:
                        pass

        solve_side()
        solve_side(invert=True)
        solve_side(vertical=True)
        solve_side(vertical=True, invert=True)

        return available

    @staticmethod
    def queen(p_x, p_y, player, only_beat=False):
        """
        :param only_beat:
        :param player:
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        beat = []
        available = Rules.rook(p_x, p_y, player)
        available += Rules.bishop(p_x, p_y, player)
        return available

    @staticmethod
    def king(p_x, p_y, player, only_beat=False):
        """
        :param only_beat:
        :param player:
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        available = []
        beat = []
        try:
            if Table.field[p_y - 1][p_x][0] != player.letter:
                available.append([p_x, p_y - 1])
        except IndexError:
            pass
        try:
            if Table.field[p_y + 1][p_x][0] != player.letter:
                available.append([p_x, p_y + 1])
        except IndexError:
            pass
        try:
            if Table.field[p_y][p_x - 1][0] != player.letter:
                available.append([p_x - 1, p_y])
        except IndexError:
            pass
        try:
            if Table.field[p_y][p_x + 1][0] != player.letter:
                available.append([p_x + 1, p_y])
        except IndexError:
            pass
        try:
            if Table.field[p_y - 1][p_x - 1][0] != player.letter:
                available.append([p_x - 1, p_y - 1])
        except IndexError:
            pass
        try:
            if Table.field[p_y - 1][p_x + 1][0] != player.letter:
                available.append([p_x + 1, p_y - 1])
        except IndexError:
            pass
        try:
            if Table.field[p_y + 1][p_x + 1][0] != player.letter:
                available.append([p_x + 1, p_y + 1])
        except IndexError:
            pass
        try:
            if Table.field[p_y + 1][p_x - 1][0] != player.letter:
                available.append([p_x - 1, p_y + 1])
        except IndexError:
            pass

        return available

    @staticmethod
    def side_available(movements, player, opposite_side=False):
        side_available = []
        if opposite_side:
            side = player.opposite
        else:
            side = player.letter
        for x in range(8):
            for y in range(8):
                if Table.field[y][x][0] == side:
                    side_available.extend(movements[Table.field[y][x][1]](x, y, player, only_beat=True))
        return side_available

    @staticmethod
    def basic_check(p_x, p_y, movements, player):
        available = []
        for turn in movements[Table.field[p_y][p_x][1]](p_x, p_y, player):
            available.append(Table.field[turn[1]][turn[0]])
        return available

    @staticmethod
    def naive_mate(enemy: 'Available turns of enemy piece', movements, player):
        # I must find exact way, which allows enemy beat my king
        Enemy = set(map(lambda elem: tuple(elem), enemy))
        side_available = set(map(tuple, Rules.side_available(movements, player)))
        return Enemy.isdisjoint(side_available)  # if True -> Mate else check


class BOT:
    def __init__(self):
        pass


if __name__ == '__main__':
    CHESS_GAME = Chess()
    CHESS_GAME.run()
