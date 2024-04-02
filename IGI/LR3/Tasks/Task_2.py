from Decorator import task_decorator


@task_decorator
def task_2():
    """
        **Lab Work 3 | Task 2**

        * Developer: Gorgun Alexander

        * Date: 29.03.2024

        Organize loop that takes integers and sums up every second of them

        The end of cycle is input of number 0
    """

    a = -1
    sum_ans = 0
    i = 0

    print("Input numbers. Last 0.")

    while a != 0:
        try:
            a = int(input())
            if i % 2:
                sum_ans += a
            i += 1
        except Exception as e:
            print(e)

    print("Sum: ", sum_ans)
