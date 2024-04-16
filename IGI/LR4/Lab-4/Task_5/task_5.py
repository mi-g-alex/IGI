import random

import numpy as np


class Task5:
    def __init__(self):
        print("Task 5. Numpy")
        n, m = (int(input('Введите длину матрицы: \n')),
                int(input('Введите ширину матрицы: \n')))
        self.arr = np.array([[random.randint(-100, 100) for _ in range(n)] for _ in range(m)])
        print('Матрица:')
        print(self.arr)
        self.sort_it()
        print('Отсортированная матрица:')
        print(self.arr)
        print('Среднее np: ')
        print(f'{np.mean(self.arr[:, -1]):<.2f}')
        print('Среднее my: ')
        print(f'{self.mean():.2f}')

    def sort_it(self):
        """Cортим матрицу"""
        self.arr = np.array(sorted(self.arr, key=lambda x: x[-1], reverse=True))

    def mean(self):
        """Среднее в ласт столбце"""
        ans = 0
        for i in self.arr:
            ans += i[-1]
        return ans / len(self.arr)
