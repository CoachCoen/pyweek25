class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def width(self):
        return self.x

    @property
    def height(self):
        return self.y

    def to_rect(self, size):
        return self.x, self.y, size.x, size.y

    def __getitem__(self, item):
        return (self.x, self.y)[item]

    def __len__(self):
        return 2

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return '<Vector>({}, {})'.format(self.x, self.y)
