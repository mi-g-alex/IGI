import math
import statistics

import matplotlib.pyplot as plt

import CheckDir


class Task3(CheckDir.CheckDirMixin):

    def __init__(self):
        super().check_dir("Task_3/img/")
        print("Task 3. Plot")
        try:
            x = float(input("Введите от -1 до 1: "))
        except ValueError as e:
            print("Не. Не то чтото...")
            return

        ans, n, lst = self.my_arcsin(x, 0.0001)
        if ans is None:
            return
        print('Посчитанный вручную результат: ', ans)
        print('Посчитанный результат с помощью модуля math: ', math.acos(x))
        print('Количество итераций: ', n)
        print(f'Среднее арифметическое: {statistics.mean(lst)}')
        print(f'Медиана: {statistics.median(lst)}')
        print(f'Мода: {statistics.mode(lst)}')
        print(f'Дисперсия: {statistics.variance(lst)}')
        print(f'СКО: {statistics.stdev(lst)}')
        self.draw(1, 1000)

    def my_arcsin(self, x: float, eps: float):
        """Мой арксин"""
        if abs(x) > 1:
            print("\nX should be in range -1..1")
            return None, None, None

        n = 0
        n_fact = 1
        n_2_fact = 1
        ans = 0
        x_2n1 = x

        new_sum = lambda: n_2_fact / (4 ** n * (n_fact * n_fact) * (2 * n + 1)) * x_2n1
        arr = []

        while new_sum() > eps:
            arr.append(ans)
            ans += new_sum()
            n += 1
            if n == 500:
                break
            n_fact *= n
            n_2_fact *= 2 * n * (2 * n - 1)
            x_2n1 *= x * x

        return ans, n, arr

    def draw(self, h, rng):
        """Функция, выполняющая построение графика с функцией варианта."""
        my_sin = [self.my_arcsin(elem, 0.001)[0] for elem in [i / rng for i in range(-rng, rng, h)]]
        math_sin = [math.asin(elem) for elem in [i / rng for i in range(-rng, rng, h)]]
        fig, ax = plt.subplots()
        ax.plot([i / rng for i in range(-rng, rng, h)], my_sin, 'red', linewidth=2, label='My')
        ax.plot([i / rng for i in range(-rng, rng, h)], math_sin, 'blue', linewidth=2, label='Math')
        ax.legend(loc='lower left')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        plt.savefig('Task_3/img/task3.png')
        plt.show()
