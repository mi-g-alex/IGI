import math
import numpy as np

from Decorator import task_decorator


@task_decorator
def task_1():
    """
    **Lab Work 3 | Task 1**

    * Developer: Gorgun Alexander

    * Date: 29.03.2024

    Decompose arcsin into a power series and compare with Math lib
    """

    def my_arcsin(x: float, eps: float) -> {float | None, int | None}:
        if abs(x) > 1:
            print("\nX should be in range -1..1")
            return None, None

        n = 0
        n_fact = 1
        n_2_fact = 1
        ans = 0
        x_2n1 = x

        new_sum = lambda: n_2_fact / (4 ** n * (n_fact * n_fact) * (2 * n + 1)) * x_2n1

        while new_sum() > eps:
            ans += new_sum()
            n += 1
            if n == 500:
                break
            n_fact *= n
            n_2_fact *= 2 * n * (2 * n - 1)
            x_2n1 *= x * x

        return ans, n

    def check_input() -> [bool | float, None | float]:
        inp = input("Input x and eps: ")
        arr = inp.split(' ')
        try:
            return float(arr[0]), float(arr[1])
        except Exception as e:
            print(e)
            return False, None

    x, eps = check_input()
    while not x:
        x, eps = check_input()

    print("-" * 101)
    str_x, str_n, str_fx, str_math_fx, str_eps = 'x', 'n', 'my arcsin(x)', 'Math arcsin(x)', 'eps'
    print(f"| {str_x:<18}| {str_n:<18}| {str_fx:<18}| {str_math_fx:<18}| {str_eps:<18}|")
    print("-" * 101)

    for x in np.arange(0, 1.1, 0.1):
        ans, n = my_arcsin(x, eps)
        m_ans = math.asin(x)
        print(f"| {x:<18.2f}| {n:<18}| {ans:<18.11f}| {m_ans:<18.11f}| {(abs(m_ans - ans)):<18.11f}|")
        print("", "-" * 100)
