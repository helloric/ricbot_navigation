import dataclasses
import math


@dataclasses.dataclass
class Vector2:
    x: float = 0.0
    y: float = 0.0

    def __init__(self, x=0.0, y=0.0, *args, **kwargs):
        self.x = x
        self.y = y

    def __getitem__(self, idx):
        if idx in [0, 'x']:
            return self.x
        elif idx in [1, 'y']:
            return self.y
        elif idx in [2, 'z']:
            # just in case someone wanted a vector3 instead
            return 0.0
        else:
            raise RuntimeError(f'unknown key "{idx}"')

    def serialize(self):
        """Serializes the vector as tuple."""
        return self.to_tuple()

    def to_tuple(self):
        """generates a tuple using the dataclasses.astuple helper function."""
        return tuple(float(i) for i in dataclasses.astuple(self))

    def __iter__(self):
        """The default iteration for vectors behaves like a list or tuple."""
        yield float(self.x)
        yield float(self.y)

    def __add__(self, o):
        if isinstance(o, Vector2):
            return Vector2(self.x + o.x, self.y + o.y)
        else:
            return Vector2(*[val + o for val in self])

    def __round__(self, num):
        return Vector2(
            round(self.x, num),
            round(self.y, num))

    def __sub__(self, o):
        if isinstance(o, Vector2):
            return Vector2(self.x - o.x, self.y - o.y)
        else:
            return Vector2(*[val - o for val in self])

    def __mul__(self, o):
        """ Scalar multiplication """
        if isinstance(o, Vector2):
            return Vector2(self.x * o.x, self.y * o.y)
        else:
            return Vector2(*[val * o for val in self])

    def __neg__(self):
        """ Returns the vector pointing in the opposite direction """
        return Vector2(-self.x, -self.y)

    def magnitude(self):
        """ Calculate the euclidean length of the vector """
        return math.sqrt(sum([val**2 for val in self]))

    def normalize(self):
        """ Normalizes the vector to have unit length """
        return Vector2(*[q / self.magnitude() for q in self])

    def null(self):
        """Check if both, x and y are 0."""
        return self.x == self.y == 0

    def copy(self):
        """create a new vector2 instance."""
        return Vector2(*self)

    @staticmethod
    def from_any(_any):
        if isinstance(_any, (Vector2)):
            return _any
        if isinstance(_any, (list, tuple, set)):
            return Vector2(*_any)
        if isinstance(_any, dict):
            return Vector2(**_any)
        raise RuntimeError('given data neither list nor dict')

    def is_close(self, other, rel_tol=0.01, abs_tol=0.01, threshold=None):
        """ Check if a Vector2 is close to another Vector2. """
        if not other:
            return False
        if isinstance(other, dict):
            x, y = other['x'], other['y']
        elif isinstance(other, (list, tuple, set)):
            x, y = other
        else:
            x, y = other.x, other.y
        if threshold:
            return abs(self.x - x) + abs(self.y + y) < threshold
        return math.isclose(
                self.x, x, rel_tol=rel_tol, abs_tol=abs_tol) and \
            math.isclose(
                self.y, y, rel_tol=rel_tol, abs_tol=abs_tol)

    def distance(self, other):
        """ Calculate the distance to the given position """
        return (self - other).magnitude()

    def midpoint(self, other):
        """Return a midpoint between the two points."""
        return Vector2((self.x + other.x) / 2, (self.y + other.y) / 2)
