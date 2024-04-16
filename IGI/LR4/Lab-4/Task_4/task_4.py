import math
from abc import ABC, abstractmethod

from matplotlib import pyplot as plt

import CheckDir


class Color:
    def __init__(self, color):
        """Функция, инициализирующая объект класса."""
        self.color = color

    @property
    def color_init(self):
        """Функция-геттер для переменной color."""
        return self.color

    @color_init.setter
    def color_init(self, new_color):
        """Функция-сеттер для переменной color."""
        self.color = new_color

    @color_init.deleter
    def color_init(self):
        """Функция-делетер для переменной color."""
        del self.color

    def __str__(self):
        """Магический метод, to_string."""
        return self.color


class GeometricFigure(ABC):

    @abstractmethod
    def square(self):
        """Функция, вычисляющая площадь фигуры."""


class Pentagon(GeometricFigure):

    def __init__(self, name, a, color):
        self.a_ = a
        self.name = name
        self.color = Color(color)

    @property
    def a(self):
        """Функция-геттер для переменной"""
        return self.a_

    @a.setter
    def a(self, a):
        """Функция-сеттер для переменной."""
        self.a_ = a

    @property
    def name(self):
        """Функция-геттер для переменной name."""
        return self.name_

    @name.setter
    def name(self, name):
        """Функция-сеттер для переменной name."""
        self.name_ = name

    def square(self):
        """Тут считаем площадь"""
        return self.a_ ** 2 * math.sqrt(25 + 10 * math.sqrt(5)) / 4

    def draw(self):
        """Тут рисуем пятиугольник"""
        try:
            dots_x = []
            dots_y = []
            r = self.a_ / 2 / math.sin(math.pi * 36 / 180)
            for i in range(0, 361, 72):
                dots_x.append(r * math.sin(math.pi * i / 180))
                dots_y.append(r * math.cos(math.pi * i / 180))

            plt.legend('', frameon=False)

            plt.plot(dots_x, dots_y)
            plt.fill(dots_x, dots_y, alpha=0.5, facecolor=self.color.color_init)

            plt.title(str(self.name_) + " площадь " + str(self.square()))
            plt.grid(True)
            plt.savefig('Task_4/img/task4.png')
            plt.show()
        except Exception as e:
            print("Чтото пошло не так...", e)


class Task4(CheckDir.CheckDirMixin):
    def __init__(self):
        super().check_dir('Task_4/img/')
        print("Task 4. Pentagon")
        a = int(input("Введите длину стороны: "))
        p = Pentagon("Pentagon", a, 'black')
        p.draw()


