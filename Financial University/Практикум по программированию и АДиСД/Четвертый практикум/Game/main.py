import pygame
from Board import Table
from Engine import Engine
from Build import Build
from Button import Button
Table = Table()


class Player:
    def __init__(self, letter='w', opposite='b', name='White'):
        self.score = 0
        self.name = name
        self.letter = letter
        self.opposite = opposite


class Main(Engine):
    """
    Creates an application
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

    def __init__(self):
        super().__init__()

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
        cls.font = pygame.font.Font(None, 22)
        pygame.display.set_caption('Chess')

    @classmethod
    def run(cls, **kwargs):
        """
        The main function for launching the application
        :param kwargs:
        :return: pygame application
        """
        while cls.running:
            cls._prepare_()
            Sound.init()
            Graphics.create_board()
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


class Graphics(Main):
    """
    The class responsible for the graphical component of the application
    """
    button_list = list()
    button2 = None
    button1 = None
    output_error = 725
    strings = []

    @classmethod
    def get_button_list(cls):
        def cancel_turn():
            print('Turn canceled')
        cls.button2 = Button((867, 45), (250, 50), (220, 220, 220), (255, 0, 0), cancel_turn, 'Отменить ход')

        cls.button_list = [cls.button2]
        return cls.button_list

    @classmethod
    def create_board(cls):  # whole process in couple
        """
        The main function for creating board and putting a pieces
        """
        cls._board_()
        cls._pieces_()

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
            cls.output = cls.font.render(string, 2, pygame.Color('red'))
            cls.pos = cls.output.get_rect(center=(super().RATIO[0] + 140, super().RATIO[1] - error))
            cls.screen.blit(cls.output, cls.pos)


class Controls(Main, Sound):
    old_piece = '--'
    p_letter = 'w' or 'b'
    any_y = None
    any_x = None
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
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if cls.any_x is not None:
                        for b in Graphics.get_button_list():
                            if cls.any_x > 7 or cls.any_y > 7:
                                break
                            if b.rect.collidepoint(pos):
                                Table.field[cls.any_y][cls.any_x] = cls.old_piece
                                Table.field[cls.y][cls.x] = cls.piece[0]
                                cls.current_player = super().BLACK if cls.p_letter == 'b' else super().WHITE
                                cls.chose = True

                cls.any_x = event.pos[0] // (cls.RATIO[0] // cls.DIMENSIONS)
                cls.any_y = event.pos[1] // (cls.RATIO[0] // cls.DIMENSIONS)

                if cls.any_x > 7 or cls.any_y > 7:
                    break
                cls.p_letter = cls.current_player.letter
                movements = {
                    'p': Rules.pawn,
                    'N': Rules.knight,
                    'B': Rules.bishop,
                    'R': Rules.rook,
                    'Q': Rules.queen,
                    'K': Rules.king
                }

                if Table.field[cls.any_y][cls.any_x] != '--' \
                        and Table.field[cls.any_y][cls.any_x][0] != cls.current_player.opposite:
                    cls.chose = True
                    coordinates = [cls.y, cls.x] = cls.any_y, cls.any_x
                    cls.piece = (Table.field[cls.any_y][cls.any_x], coordinates)
                if cls.x or cls.y is not None:
                    available = movements[cls.piece[0][1]](cls.x, cls.y, cls.current_player)

                    if cls.chose:  # figure chosen
                        print(available)
                        if [cls.any_x, cls.any_y] in available and cls.p_letter == cls.piece[0][0]:  # movement of piece
                            print('PASSED')
                            print(cls.piece[0][1])
                            if Table.field[cls.any_y][cls.any_x][0] == cls.current_player.opposite:
                                super().beat_sound.play()
                                Graphics.strings.append(Graphics.info_gainer(Table.field[cls.any_y][cls.any_x]))
                            elif cls.piece[0][1] == 'N':
                                super().Knight_move.play()
                            elif Table.field[cls.any_y][cls.any_x] == '--':
                                super().move_sound.play()
                            cls.old_piece = Table.field[cls.any_y][cls.any_x]
                            Table.field[cls.any_y][cls.any_x] = cls.piece[0]

                            Table.field[cls.piece[1][0]][cls.piece[1][1]] = '--'

                            cls.chose = False
                            cls.current_player = super().BLACK if cls.p_letter == 'w' else super().WHITE
                            # Graphics.print_info(f"{cls.current_player.name}'s turn")
                        print(Table.field[cls.any_y][cls.any_x][0], cls.current_player.opposite)

                print(f'x = {cls.any_x}, y = {cls.any_y}')


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
        if Table.field[p_y + 1][p_x] == '--':
            if p_y == 1:
                available.append([p_x, p_y + 2])
                available.append([p_x, p_y + 1])
            elif Table.field[p_y][p_x][0] == 'b':
                available.append([p_x, p_y + 1])
        if Table.field[p_y - 1][p_x] == '--':
            if p_y == 6:
                available.append([p_x, p_y - 1])
                available.append([p_x, p_y - 2])
            elif Table.field[p_y][p_x][0] == 'w':
                available.append([p_x, p_y - 1])
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
                        print(Table.field[p_y - y][p_x - x])
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
    CHESS_GAME = Engine()
    CHESS_GAME.run(size='medium')
