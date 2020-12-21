"""
Класс визуализации популяции на графике
"""

from universe import Universe
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# тестовые параметры
GRID_SIZE = 50
INITIAL_PREDATORS = 50
INITIAL_PREYS = 50

# тестовый мир
u = Universe(GRID_SIZE, INITIAL_PREDATORS, INITIAL_PREYS)


class plot_graph:
    def __init__(self, u):
        # инициализация графика
        self.fig = plt.figure('Хищник-Жертва модель')
        self.ax = self.fig.add_subplot(111)
        self.plot_x = []
        self.plot_y1 = []
        self.plot_y2 = []
        self.u = u
        self.ani = ''

    def animate(self, i):
        self.u.move_animals()
        self.u.prepare_next_round()
        self.plot_x.append(i)
        self.plot_y1.append(len(self.u.predators))
        self.plot_y2.append(len(self.u.preys))
        self.ax.clear()
        self.ax.plot(self.plot_x, self.plot_y1, 'r', label='Хищник')
        self.ax.plot(self.plot_x, self.plot_y2, 'g', label='Жертва')
        self.ax.set_xlabel('Время')
        self.ax.set_ylabel('Популяция')
        self.ax.legend()

    def run(self):
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=1000)
        self.ani.save('animation.gif', fps=10)


if __name__ == "__main__":
    p = plot_graph(u)
    p.run()
