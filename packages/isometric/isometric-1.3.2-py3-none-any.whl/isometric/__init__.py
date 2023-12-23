import math as _math
import typing as _typing


class _Description(_typing.NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0



class _Digest(_typing.NamedTuple):
    x: float = 0.0
    y: float = 0.0
    def radius(self) -> float:
        return ((a ** 2) for a in self) ** .5
    def angle(self) -> float:
        try:
            ratio = self.x / self.radius()
        except ZeroDivisionError:
            return float('nan')
        ans = _math.acos(ratio)
        if self.y < 0:
            ans *= -1
        return ans

    




class Vector:


    def __abs__(self):
        desc = self.description()
        values = list(set(desc) - {0})
        if len(values) == 1:
            return abs(values.pop())
        return self.digest().radius()
    
    def __add__(self, other):
        cls = type(self)
        if type(other) is not cls:
            raise TypeError
        return cls(0, self._y + other._y, self._z + other._z)

    def __bool__(self):
        return any(self.description())

    def __div__(self, other):
        cls = type(self)
        return cls(
            0, 
            self._y / other, 
            self._z / other,
        )

    def __eq__(self, other):
        cls = type(self)
        if type(other) is not cls:
            return False
        return self.description() == other.description()

    def __float__(self):
        return float('nan') if self else .0

    def __hash__(self):
        return self.description().__hash__()

    def __init__(self, *args, **kwargs):
        desc = _Description(*args, **kwargs)
        for a in desc:
            if type(a) is not int:
                raise TypeError
        self._y = desc.y - desc.x
        self._z = desc.z - desc.x

    def __int__(self):
        return int(float(self))
    
    def __mul__(self, other):
        cls = type(self)
        if type(other) is not cls:
            return cls(
                0, 
                self._y * other, 
                self._z * other,
            )
        return (
            (self._y * other._y)
            + (self._z * other._z)
            + (-.5 * self._y * other._z)
            + (-.5 * self._z * other._y)
        )

    def __neg__(self):
        cls = type(self)
        return cls(0, -self._y, -self._z)

    def __pow__(self, other):
        if type(other) is not int:
            raise TypeError
        if other < 0:
            raise ValueError
        ans = 1
        for i in range(other):
            ans *= self
        return ans

    def __rmul__(self, other):
        cls = type(self)
        return cls(
            0, 
            other * self._y, 
            other * self._z,
        )

    def __sub__(self, other):
        return self + (-other)


    def description(self, tare='x'):
        tare = {
            'x':0,
            'y':1,
            'z':2,
        }[tare]
        if tare == 0:
            return _Description(0, self._y, self._z)
        if tare == 1:
            return _Description(-self._y, 0, self._z - self._y)
        if tare == 2:
            return _Description(-self._z, self._y - self._z, 0)
        raise NotImplementedError
    
    def digest(self):
        x = (3 ** .5) * .5 * self._y
        y = (-.5 * self._y) + self._z
        ans = _Digest(x, y)
        return ans
    
    def factorize(self):
        scale = _math.gcd(
            abs(self._y), 
            abs(self._z),
        )
        hint = self / scale
        return (scale, hint)
    
    def hflip(self):
        cls = type(self)
        ans = cls(self._y, 0, self._z)
        return ans
    
    @classmethod
    def linear_dependence(cls, *vectors):
        errors = list()
        for v in vectors:
            if type(v) is not cls:
                errors.append(TypeError(v))
        if len(errors):
            raise ExceptionGroup("Non-Vectors given!", errors)
        if len(vectors) > 2:
            return True
        if len(vectors) < 2:
            return not all(vectors)
        v, w = vectors
        return (v._y * w._z) == (v._z * w._y)
    
    def rotate(self, amount):
        cls = type(self)
        if type(amount) is not int:
            raise TypeError
        vector = self
        if amount % 2:
            amount += 3
            vector = -vector
        amount %= 6
        if amount == 0:
            return cls(0, vector._y, vector._z)
        if amount == 2:
            return cls(vector._z, 0, vector._y)
        if amount == 4:
            return cls(vector._y, vector._z, 0)
        raise NotImplementedError

    def vflip(self):
        cls = type(self)
        ans = cls(-self._y, 0, -self._z)
        return ans


