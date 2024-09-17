# create a class Rectangle
class Rectangle:
    # __init__ method that takes width and height as parameters
    def __init__(self, width, length):
        self.width = width
        self.length = length
    # perimeter method that returns the perimeter of the rectangle
    def area(self):
        return self.width * self.length

my_rectangle = Rectangle(3, 5)

print(f'The area of the rectangle is {my_rectangle.area()}.')