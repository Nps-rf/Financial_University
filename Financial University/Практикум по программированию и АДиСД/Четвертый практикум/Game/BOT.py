class BOT:  # TODO
    __instance = None

    def __call__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __del__(self):
        BOT.__instance = None

    def __init__(self):
        pass

    def read_game(self):
        pass

    def play_game(self):
        pass