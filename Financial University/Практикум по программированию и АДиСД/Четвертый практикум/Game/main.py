import pygame
from Board import Table
from Build import Build
from Button import Button
Table = Table()


class Player:
    def __init__(self, letter='w', opposite='b', name='White'):
        self.score = 0
        self.name = name
        self.letter = letter
        self.opposite = opposite


class Main:
    """
    Creates an application
    Abbreviations scheme:
    ◈ First letter -> color of piece
    ◈ Second letter -> exact piece
    Example:
        ◈ wK -> White King
    images:
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
    FPS = 30
    WHITE = Player()
    BLACK = Player(letter='b', opposite='w', name='Black')
    output = pygame.font.Font.render
    RATIO = (WIDTH, HEIGHT) = (720, 720)
    DIMENSIONS = 8
    SQUARE_SIZE = WIDTH // DIMENSIONS
    expand = 6 * 2  # The error for the screen resolution (so that the figures do not move out)

    @classmethod
    def _prepare_(cls):
        """
        Function that prepares an application for launch
        """
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        cls.screen = pygame.display.set_mode((cls.RATIO[0] + (cls.RATIO[0] // 3 + 50), cls.RATIO[1]))
        cls.screen.fill('white')
        pygame.draw.rect(
            cls.screen,
            pygame.Color('dark grey'),
            pygame.Rect(
                5,  # Horizontal coordinate
                0,  # Vertical coordinate
                cls.RATIO[0],  # Size of square
                cls.RATIO[0])  # Size of square
        )
        cls.font = pygame.font.Font(None, 23)
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
            Controls.run_controls()
            Graphics.print_info()
            for b in Graphics.get_button_list():
                b.draw(cls.screen)
            pygame.display.update()


class Sound:
    @classmethod
    def init(cls):
        pygame.mixer.init()
        cls.move_sound = pygame.mixer.Sound('Sound/move of piece.ogg')
        cls.beat_sound = pygame.mixer.Sound('Sound/peace beaten.ogg')
        cls.Knight_move = pygame.mixer.Sound('Sound/Knight movement.ogg')
        cls.Pawn = pygame.mixer.Sound('Sound/Pawn.ogg')
        cls.Rook = pygame.mixer.Sound('Sound/Rook.ogg')
        cls.Knight = pygame.mixer.Sound('Sound/Knight.ogg')
        cls.Queen = pygame.mixer.Sound('Sound/Queen.ogg')
        cls.Castle = pygame.mixer.Sound('Sound/Castle.ogg')
        cls.Bishop = pygame.mixer.Sound('Sound/Bishop.ogg')
        cls.King = pygame.mixer.Sound('Sound/King.ogg')


class Graphics(Main):
    """
    The class responsible for the graphical component of the application
    """
    available_moves = list()
    button_list = list()
    button1 = Button
    output_error = 670
    strings = []

    @classmethod
    def get_button_list(cls):
        def cancel_turn():
            print('Turn canceled')
        cls.button1 = Button((867, 45), (250, 50), (220, 220, 220), (255, 0, 0), cancel_turn, 'Отменить ход')

        cls.button_list = [cls.button1]
        return cls.button_list

    @classmethod
    def board_graphics(cls):  # whole process in couple
        """
        The main function for creating board and putting a pieces
        """
        cls._board_()
        cls._pieces_()
        if len(cls.available_moves) > 0:
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
        for square in cls.available_moves:
            color = (0, 150, 0, 120) if Table.field[square[1]][square[0]] == '--' else (150, 0, 0, 120)
            available_move = pygame.Surface((cls.RATIO[0], cls.RATIO[0]), pygame.SRCALPHA)
            pygame.draw.rect(
                available_move,
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
            cls.pos = cls.output.get_rect(center=(super().RATIO[0] + 140, super().RATIO[1] - error))
            cls.screen.blit(cls.output, cls.pos)


class Controls(Main, Sound):
    history = []
    old_piece = '--'
    row = None
    column = None
    current_player = Main.WHITE
    chose = False
    piece = ('--', [-1, -1])
    x = None
    y = None

    @classmethod
    def run_controls(cls):
        cls._look4click_()

    @classmethod
    def _look4click_(cls):
        """
        Checks whether the user clicked on the cross (or other place)
        It's the biggest trash i've ever made
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Main.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # return section
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for b in Graphics.get_button_list():
                        if b.rect.collidepoint(pos):
                            for number, turn in enumerate(cls.history[::-1]):
                                x_return = turn[0][0]
                                y_return = turn[0][1]
                                Table.field[y_return][x_return] = turn[2]
                                Table.field[turn[1][1]][turn[1][0]] = turn[3]
                                super().move_sound.play()
                                print(turn[4])
                                cls.current_player = super().BLACK if turn[4] == 'b' else super().WHITE
                                cls.chose = True
                                cls.already_returned = True
                                del cls.history[-1]
                                break
                # move&beat section
                cls.column = event.pos[0] // (cls.RATIO[0] // cls.DIMENSIONS)
                cls.row = event.pos[1] // (cls.RATIO[0] // cls.DIMENSIONS)

                if event.pos[0] // (cls.RATIO[0] // cls.DIMENSIONS) > 7 or \
                        event.pos[1] // (cls.RATIO[0] // cls.DIMENSIONS) > 7:
                    break
                else:
                    cls.column = event.pos[0] // (cls.RATIO[0] // cls.DIMENSIONS)
                    cls.row = event.pos[1] // (cls.RATIO[0] // cls.DIMENSIONS)
                movements = {
                    'p': Rules.pawn,
                    'N': Rules.knight,
                    'B': Rules.bishop,
                    'R': Rules.rook,
                    'Q': Rules.queen,
                    'K': Rules.king
                }
                sounds = {
                    'p': super().Pawn.play,
                    'N': super().Knight.play,
                    'B': super().Bishop.play,
                    'R': super().Rook.play,
                    'Q': super().Queen.play,
                    'K': super().King.play
                }

                # get coordinates and misc
                if Table.field[cls.row][cls.column] != '--' \
                        and Table.field[cls.row][cls.column][0] != cls.current_player.opposite:
                    cls.chose = True
                    coordinates = [cls.y, cls.x] = cls.row, cls.column
                    cls.piece = (Table.field[cls.row][cls.column], coordinates)

                # play sound of chosen piece and look for all squares available to move
                if cls.x or cls.y is not None:
                    available = movements[cls.piece[0][1]](cls.x, cls.y, cls.current_player)
                    if Table.field[cls.row][cls.column][1] in sounds.keys() \
                            and Table.field[cls.row][cls.column][0] != cls.current_player.opposite:
                        if len(Graphics.available_moves) > 0:
                            Graphics.available_moves.clear()
                        sounds[Table.field[cls.row][cls.column][1]]()  # playing sound
                        Graphics.available_moves += available  # show available moves

                    if cls.chose:  # figure chosen and can move
                        print('Squares you can move -> ', *available)
                        # movement of piece
                        if [cls.column, cls.row] in available \
                                and cls.current_player.letter == cls.piece[0][0]:

                            if Table.field[cls.row][cls.column][0] == cls.current_player.opposite:
                                super().beat_sound.play()
                                Graphics.strings.append(Graphics.info_gainer(Table.field[cls.row][cls.column]))

                            elif cls.piece[0][1] == 'N':
                                super().Knight_move.play()

                            elif Table.field[cls.row][cls.column] == '--':
                                super().move_sound.play()

                            cls.old_x_y = [cls.column, cls.row]

                            cls.old_piece = Table.field[cls.row][cls.column] \
                                if Table.field[cls.row][cls.column] == '--' else '--'

                            cls.history.append([[cls.piece[1][1], cls.piece[1][0]],  # from
                                                [cls.column, cls.row],  # to
                                                cls.piece[0],  # who moves
                                                Table.field[cls.row][cls.column],  # from-old
                                                cls.current_player.letter])  # Who moved

                            Table.field[cls.row][cls.column] = cls.piece[0]

                            Table.field[cls.piece[1][0]][cls.piece[1][1]] = cls.old_piece
                            ############################################################################################
                            cls.chose = False
                            cls.current_player = super().BLACK if cls.current_player.letter == 'w' else super().WHITE
                            cls.x4return = event.pos[0] // (cls.RATIO[0] // cls.DIMENSIONS)
                            cls.y4return = event.pos[1] // (cls.RATIO[0] // cls.DIMENSIONS)
                            if len(Graphics.available_moves) > 0 :
                                Graphics.available_moves.clear()
                            ############################################################################################

                print(f'x = {cls.column}, y = {cls.row}')


class Rules:
    @staticmethod
    def pawn(p_x, p_y, *_):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        # Movement section
        available = []
        try:
            if Table.field[p_y + 1][p_x] == '--':
                if p_y == 1:
                    available.append([p_x, p_y + 2])
                    available.append([p_x, p_y + 1])
                elif Table.field[p_y][p_x][0] == 'b':
                    available.append([p_x, p_y + 1])
        except IndexError:
            pass
        try:
            if Table.field[p_y - 1][p_x] == '--':
                if p_y == 6:
                    available.append([p_x, p_y - 1])
                    available.append([p_x, p_y - 2])
                elif Table.field[p_y][p_x][0] == 'w':
                    available.append([p_x, p_y - 1])
        except IndexError:
            pass
        # White Beat section
        if Table.field[p_y][p_x][0] == 'w':
            try:
                if Table.field[p_y - 1][p_x - 1][0] == 'b':
                    available.append([p_x - 1, p_y - 1])
            except IndexError:
                pass

            try:
                if Table.field[p_y - 1][p_x + 1][0] == 'b':
                    available.append([p_x + 1, p_y - 1])
            except IndexError:
                pass

        # Black Beat section?
        if Table.field[p_y][p_x][0] == 'b':
            try:
                if Table.field[p_y + 1][p_x - 1][0] == 'w':
                    available.append([p_x - 1, p_y + 1])
            except IndexError:
                pass

            try:
                if Table.field[p_y + 1][p_x + 1][0] == 'w':
                    available.append([p_x + 1, p_y + 1])
            except IndexError:
                pass

        return available

    @staticmethod
    def knight(p_x, p_y, player):
        """
        :param player:
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        table = Table.field
        available = []

        # leftward
        try:
            if table[p_y - 1][p_x - 2][0] != player.letter:
                available.append([p_x - 2, p_y - 1])
        except IndexError:
            pass
        try:
            if table[p_y + 1][p_x - 2][0] != player.letter:
                available.append([p_x - 2, p_y + 1])
        except IndexError:
            pass
        # above
        try:
            if table[p_y - 2][p_x - 1][0] != player.letter:
                available.append([p_x - 1, p_y - 2])
        except IndexError:
            pass
        try:
            if table[p_y - 2][p_x + 1][0] != player.letter:
                available.append([p_x + 1, p_y - 2])
        except IndexError:
            pass

        # on the right
        try:
            if table[p_y - 1][p_x + 2][0] != player.letter:
                available.append([p_x + 2, p_y - 1])
        except IndexError:
            pass
        try:
            if table[p_y + 1][p_x + 2][0] != player.letter:
                available.append([p_x + 2, p_y + 1])
        except IndexError:
            pass
        # below
        try:
            if table[p_y + 2][p_x - 1][0] != player.letter:
                available.append([p_x - 1, p_y + 2])
        except IndexError:
            pass
        try:
            if table[p_y + 2][p_x + 1][0] != player.letter:
                available.append([p_x + 1, p_y + 2])
        except IndexError:
            pass
        return available

    @staticmethod
    def bishop(p_x, p_y, player):
        """
        :param player:
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        available = []

        def solve_side(upper=True, left=True):
            no_way = False
            for x, y in zip(range(1, 8 + 1), range(1, 8 + 1)):
                if not upper:
                    y = -y
                if not left:
                    x = -x
                if no_way:
                    break
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
    def rook(p_x, p_y, *_):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        pass

    @staticmethod
    def queen(p_x, p_y, *_):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        pass

    @staticmethod
    def king(p_x, p_y, *_):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        pass


if __name__ == '__main__':
    CHESS_GAME = Main()
    CHESS_GAME.run()
