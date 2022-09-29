from shape import Shape


class Circle(Shape):
    def __init__(self, color, rad):
        """
        gets the color and the radios of the circle
        :param color: str
        :param rad: int
        """
        super().__init__()
        self.rad = rad
        self.set_color(color)
        self.set_area(rad ** 2 * 3.14)
        self.set_perimeter(rad * 2 * 3.14)

    def get_rad(self):
        """
        :return: the object's radios
        """
        return self.rad


c = Circle("red", 4)
assert c.get_color() == "red"
assert c.get_rad() == 4
