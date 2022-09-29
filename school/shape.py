class Shape:
    def __init__(self, color=None, area=None, perimeter=None):
        """
        :param color: none
        :param area: none
        :param perimeter: none
        """
        self.color = color
        self.area = area
        self.perimeter = perimeter

    def __str__(self):
        """
        prints the object
        """
        return f'color: {self.color}, area: {self.area}, perimeter: {self.perimeter}'

    def get_color(self):
        """
        :return: color of the object
        """
        return self.color

    def get_area(self):
        """
        :return: area of the object
        """
        return self.area

    def get_perimeter(self):
        """
        :return: perimeter of the object
        """
        return self.perimeter

    def set_color(self, color):
        """
        :param color: str
        :return: sets the object color to a new one
        """
        self.color = color

    def set_area(self, area):
        """
        :param area: int
        :return: sets the object area to a new one
        """
        self.area = area

    def set_perimeter(self, perimeter):
        """
        :param perimeter: int
        :return: sets the object perimeter to a new one
        """
        self.perimeter = perimeter
