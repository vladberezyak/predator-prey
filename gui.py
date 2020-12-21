"""
Визуализация модели
"""
from universe import Universe
from animated_plotter import plot_graph
import time
import matplotlib.pyplot as plt
import pygame
import tkinter as tk

class GuiMode:
    def __init__(self):
        self.root = tk.Tk(className='Модель Хищник-Жертва')
        self.root.geometry('300x270')
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.initialPred = tk.IntVar()
        self.initialPred.set(100)
        self.initialPrey = tk.IntVar()
        self.initialPrey.set(50)
        self.want_to_run = False
        self.runButton = tk.Button(self.frame, text='Запуск!', command=self.runner, bg='orange', width=6, height=2)
        self.initialPreyEntry = tk.Entry(self.frame, textvariable=self.initialPrey, width=7)
        self.label3 = tk.Label(self.frame, text='Начальное количество жертв:')
        self.initialPredEntry = tk.Entry(self.frame, textvariable=self.initialPred, width=7)
        self.label2 = tk.Label(self.frame, text='Начальное количество хищников:')
        self.initial_prey = self.initialPrey.get()
        self.initial_pred = self.initialPred.get()
        self.output_form = 'animation'

    def runner(self):
        self.root.destroy()
        self.want_to_run = True

    def setLabel(self):
        self.label2.grid(row=2, column=1)
        self.initialPredEntry.grid(row=2, column=2)
        self.label3.grid(row=3, column=1)
        self.initialPreyEntry.grid(row=3, column=2)
        self.runButton.grid(row=5, column=2)
        self.root.mainloop()

    def run(self):
        self.setLabel()
        start_time = time.time()
        DISPLAY_SIZE = 700
        ROUNDS_PER_SEC = 1
        # инициализация мира
        self.u = Universe(50, self.initial_pred, self.initial_prey)
        TILE_SIZE = (DISPLAY_SIZE - 300) / 50

        # инициализация pygame
        pygame.init()
        screen = pygame.display.set_mode((DISPLAY_SIZE - 300, DISPLAY_SIZE))
        pygame.display.set_caption('Модель Хищник-Жертва')
        clock = pygame.time.Clock()
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)

        pygame.font.init()
        font = pygame.font.SysFont('Arial', 18)
        text = font.render("Хищников:", True, (255, 0, 0))
        text_two = font.render("Жертв:", True, (0, 255, 0))
        # график
        predators = []
        preys = []

        # переменная отвечающая за запуск модели
        want_to_run = True
        times = []
        current_time = 0
        lasttime = 100
        lastx = 80
        lasty = 500
        while want_to_run:
            current_time = int(time.time() - start_time)
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    want_to_run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        want_to_run = False

            # логика
            self.u.move_animals()
            self.u.prepare_next_round()
            if current_time > lasttime:
                times.append(current_time)
                predators.append(len(self.u.predators))
                preys.append(len(self.u.preys))
            # Графика
            screen.fill(BLACK)

            count = font.render(str(len(self.u.predators)), True, (255, 0, 0))
            screen.blit(text, (0, 510))
            screen.blit(count, (75, 510))
            count = font.render(str(len(self.u.preys)), True, (0, 255, 0))
            screen.blit(text_two, (0, 490))
            screen.blit(count, (75, 490))

            # график
            for predator in self.u.predators:
                pygame.draw.rect(screen, RED,
                                 (predator.cell.x * TILE_SIZE, predator.cell.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            for prey in self.u.preys:
                pygame.draw.rect(screen, GREEN,
                                 (prey.cell.x * TILE_SIZE, prey.cell.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            for timez in times:
                if timez > 2:
                    if predators[timez - 2] < 110:
                        pygame.draw.line(screen, RED,
                                         [int((timez * 2) + 101),
                                          int((predators[timez - 1] * (-1)) + 600)],
                                         [int((timez * 2) + 102),
                                          int((predators[timez - 2] * (-1)) + 600)], 3)
                    else:
                        pygame.draw.line(screen, RED,
                                         [int((timez * 2) + 101),
                                          480],
                                         [int((timez * 2) + 102),
                                          480], 3)

                    if preys[timez - 2] < 110:
                        pygame.draw.line(screen, GREEN,
                                         [int((timez * 2) + 101),
                                          int((preys[timez - 1] * (-1)) + 600)],
                                         [int((timez * 2) + 102),
                                          int((preys[timez - 2] * (-1)) + 600)], 3)
                    else:
                        pygame.draw.line(screen, GREEN,
                                         [int((timez * 2) + 101),
                                          480],
                                         [int((timez * 2) + 102),
                                          480], 3)

            pygame.display.flip()
            clock.tick(ROUNDS_PER_SEC)
            lasttime = current_time

        plt.figure(1)
        plt.plot(times, predators, 'r', lw=2, label='хищник')
        plt.plot(times, preys, 'g', lw=2, label='жертва')
        plt.xlabel('итераций')
        plt.ylabel('популяция')
        plt.legend()
        plt.show()
        plotsave = plot_graph(self.u)
        plotsave.run()
        pygame.quit()


if __name__ == '__main__':
    GuiMode().run()
