import random
from Rectangle import Rectangle
from Square import Square
from circle import Circle


class Container:
    def __init__(self):
        """
        representation..
        """
        self.storage = []
        self.color_list = ["red", "blue", "green", "yellow"]

    def generate(self, x, mini, maxi):
        """
        generates a random shape x times with the minimum and maximum size range,
        generates a random color too then appends the object to the list
        :param x: int
        :param mini: int
        :param maxi: int
        :return: list with all the objects
        """
        for i in range(0, x):
            shape = random.randint(0, 2)
            if shape == 0:
                side_a = random.randint(mini, maxi)
                side_b = random.randint(mini, maxi)
                color = random.randint(0, 3)
                color = self.color_list[color]
                shape = Rectangle(color, side_a, side_b)

            elif shape == 1:
                radios = random.randint(mini, maxi)
                color = random.randint(0, 3)
                color = self.color_list[color]
                shape = Circle(color, radios)

            else:
                side_a = random.randint(mini, maxi)
                color = random.randint(0, 3)
                color = self.color_list[color]
                shape = Square(color, side_a, side_a)

            self.storage.append(shape)

    def sum_areas(self):
        """
        Sums up the sums of the areas
        :return: int - sum of the areas
        """
        s_areas = 0
        for i in range(0, len(self.storage)):
            s_areas += self.storage[i].get_area()
        return s_areas

    def sum_perimeters(self):
        """
        Sums up the sums of the perimeters
        :return: int - sum of the perimeters
        """
        s_perimeters = 0
        for i in range(0, len(self.storage)):
            s_perimeters += self.storage[i].get_perimeter()
        return s_perimeters

    def count_colors(self):
        """
        colors dictionary that count the amount of every color
        :return: dictionary with the amounts of each color
        """
        colors_dict = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "yellow": 0
        }
        for i in range(0, len(self.storage)):
            color = self.storage[i].get_color()
            if color in colors_dict.keys():
                colors_dict[color] = colors_dict.get(color) + 1
        return colors_dict
    