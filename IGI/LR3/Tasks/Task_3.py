from Decorator import task_decorator


@task_decorator
def task_3():
    """
        **Lab Work 3 | Task 3**

        * Developer: Gorgun Alexander

        * Date: 29.03.2024

        Organize loop that takes integers and sums up every second of them

        In line entered from keyboard, count number of digits.
    """

    a = input("Input string: ")
    print("Number of digits: ", len([i for i in a if '0' <= i <= '9']))
