from shape import Shape


class Rectangle(Shape):
    def __init__(self, color, a, b):
        """
        gets the first side as a .and the second as b and the color
        :param color: str
        :param a: int
        :param b: int
        """
        super().__init__()
        self.set_color(color)
        self.set_area(a * b)
        self.set_perimeter((a + b) * 2)
        self.side_a = a
        self.side_b = b

    def get_side_a(self):
        """
        :return: side_a
        """
        return self.side_a

    def get_side_b(self):
        """
        :return: side_b
        """
        return self.side_b

    def create(self, r):
        """
        creates a new shape with the side_a and the side_b combined as his new sides.
        :param r:
        :return:
        """
        side_a = self.side_a + r.get_rid_a()
        side_b = self.side_b + r.get_rid_b()
        area = side_b * side_a
        perimeter = 2 * (side_b + side_a)
        s = Shape(color=self.color, area=area, perimeter=perimeter)
        return s


r = Rectangle("red", 2, 3)
assert r.get_color() == "red"
assert r.get_side_a() == 2
assert r.get_side_b() == 3
