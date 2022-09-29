from Rectangle import Rectangle


class Square(Rectangle):
    def __init__(self, color, a, b):
        """
        gets the first side as a. and the second as b and the color
        :param color: str
        :param a: int
        :param b: int
        """
        super().__init__(color=color, a=a, b=b)
        self.side_a = a
        self.side_b = b
        if self.side_a is not self.side_b:
            raise Exception("not a square!(a != b)")
        self.set_color(color)
        self.set_area(a * b)
        self.set_perimeter((a + b) * 2)


s = Square("red", 2, 2)
assert s.get_color() == "red"
assert s.get_side_a() == s.get_side_b() == 2


