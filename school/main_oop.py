from shape_storage import Container


def main():
    """
    main
    """
    my_container = Container()
    my_container.generate(20, 3, 8)
    print("total area:", my_container.sum_areas())
    print("total perimeter:", my_container.sum_perimeters())
    print("colors:", my_container.count_colors())


if __name__ == '__main__':
    main()
