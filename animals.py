"""
Классы животных
"""

import numpy.random as npr


class Animal():
    def __init__(self, master, species, cell):
        self.MAX_AGE = 20
        self.MAX_HUNGER = 6
        self.PROLIFERATE_MIN_AGE = 10
        self.PROLIFERATE_MAX_AGE = 18
        self.PROLIFERATE_INTERVAL = 3
        self.master = master
        self.species = species
        self.cell = cell
        self.age = 0
        self.already_moved = False
        self.proliferated_since = 1000000
        cell.contained_animal = self

        
    def die(self):
        self.cell.contained_animal = None
        if self in self.master.preys:
            self.master.preys.remove(self)
        elif self in self.master.predators:
            self.master.predators.remove(self)
            
            
    def check_proliferation(self):
        if self.age >= self.PROLIFERATE_MIN_AGE and self.age <= self.PROLIFERATE_MAX_AGE and self.proliferated_since > self.PROLIFERATE_INTERVAL:
            self.proliferate()


    def get_neighbouring_cells(self):
        neighbouring_cells = []
        if self.cell.x > 0:
            neighbouring_cells.append(self.master.cells[self.cell.x-1][self.cell.y])
        if self.cell.x < self.master.SIZE-1:
            neighbouring_cells.append(self.master.cells[self.cell.x+1][self.cell.y])
        if self.cell.y > 0:
            neighbouring_cells.append(self.master.cells[self.cell.x][self.cell.y-1])
        if self.cell.y < self.master.SIZE-1:
            neighbouring_cells.append(self.master.cells[self.cell.x][self.cell.y+1])
        return neighbouring_cells




class Predator(Animal):
    def __init__(self, master, cell):
        Animal.__init__(self, master, 'predator', cell)
        self.not_eaten_since = 0
        
        
    def move_to_cell(self, new_cell):
        if not self.already_moved:
            self.cell.contained_animal = None
            self.cell = new_cell
            if isinstance(self.cell.contained_animal, Prey):
                self.eat(self.cell.contained_animal)
            else:
                pass
            self.already_moved = True
            self.cell.contained_animal = self
            

    def proliferate(self):
        neighbours = [cell for cell in self.get_neighbouring_cells() if cell.contained_animal == None]
        if len(neighbours) != 0:
            kid_cell = npr.choice(neighbours)
            self.master.predators.append(Predator(self.master, kid_cell))
            self.proliferated_since = 0
            
            
    def check_death(self):
        if self.age > self.MAX_AGE:
            self.die()
        if self.not_eaten_since > self.MAX_HUNGER:
            self.die()
                
                
    def eat(self, prey):
        self.not_eaten_since = 0
        prey.die()

class Prey(Animal):
    def __init__(self, master, cell):
        Animal.__init__(self, master, 'prey', cell)
        
        
    def move_to_cell(self, new_cell):
        if not self.already_moved:
            self.cell.contained_animal = None
            self.cell = new_cell
            self.already_moved = True
            self.cell.contained_animal = self
            
            
    def proliferate(self):
        neighbours = [cell for cell in self.get_neighbouring_cells() if cell.contained_animal == None]
        if len(neighbours) != 0:
            kid_cell = npr.choice(neighbours)
            self.master.preys.append(Prey(self.master, kid_cell))
            self.proliferated_since = 0

            
    def check_death(self):
        if self.age > self.MAX_AGE:
            self.die()

        
