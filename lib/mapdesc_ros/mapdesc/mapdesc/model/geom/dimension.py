import dataclasses


@dataclasses.dataclass
class Dimension:
    # Dimensions in meter, defaults to a 1x1x1 meter cube
    width: float = 1.0
    length: float = 1.0
    height: float = 1.0

    def __init__(self, width=1.0, length=1.0, height=1.0, *_, **__):
        self.width = width
        self.length = length
        self.height = height

    def __iter__(self):
        """ Helper to create a tuple from this """
        yield float(self.width)
        yield float(self.length)
        yield float(self.height)

    def __add__(self, o):
        if isinstance(o, Dimension):
            return Dimension(
                self.width + o.width,
                self.length + o.length,
                self.height + o.height)
        else:
            return Dimension(
                self.width + o,
                self.length + o,
                self.height + o)

    def __sub__(self, o):
        if isinstance(o, Dimension):
            return Dimension(
                self.width - o.width,
                self.length - o.length,
                self.height - o.height)
        else:
            return Dimension(
                self.width - o,
                self.length - o,
                self.height - o)

    def __mul__(self, o):
        if isinstance(o, Dimension):
            return Dimension(
                self.width * o.width,
                self.length * o.length,
                self.height * o.height)
        else:
            return Dimension(
                self.width * o,
                self.length * o,
                self.height * o)

    def __neg__(self):
        return Dimension(-self.width, -self.length, -self.height)

    def null(self):
        """check if all sides are 0."""
        return self.width == self.height == self.length == 0.0

    def copy(self):
        """create new Dimension instance with same data."""
        return Dimension(self.width, self.length, self.height)
