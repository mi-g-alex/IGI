import os


def task_decorator(func):
    def new_fun(*args, **kwargs):
        func(*args, **kwargs)
        print("\n\nPress return to continue...")
        input()
        os.system('clear')

    return new_fun
