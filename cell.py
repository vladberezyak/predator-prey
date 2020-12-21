"""
Класс ячеек
"""


class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.contained_animal = None
        
        
    def show(self):
        print(('x =', self.x))
        print(('y =', self.y))