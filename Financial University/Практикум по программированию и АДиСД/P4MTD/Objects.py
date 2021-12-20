class Table:
    def __init__(self, header=None):
        if header is None:
            header = []
        self.header = header
        self.fields = []

    def __iter__(self):
        for field in self.fields:
            yield field

    def append(self, field: dict):
        self.fields.append(field)

    def set_header(self, header):
        self.header = header
