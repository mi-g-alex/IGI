from Decorator import task_decorator


@task_decorator
def task_5():
    """
        **Lab Work 3 | Task 5**

        * Developer: Gorgun Alexander

        * Date: 29.03.2024

        Find number of positive even list items and the sum of list items located after last element equal to zero
    """

    def inp():
        a = input("Input all number by space in one line: ")
        try:
            list_of_str = a.split(' ')
            list_of_number = [float(i) for i in list_of_str if i != '']
            return list_of_number
        except Exception as e:
            print(e)
            return inp()

    def found0(t: list[float]) -> int:
        for j in range(len(t) - 1, -1, -1):
            if t[j] == 0:
                return j
        return -1

    input_str = inp()

    if found0(input_str) < 0:
        print("Not 0 found...")
        input_str = inp()

    tmp = input_str[(found0(input_str) + 1)::]
    input_str = tmp

    cnt = 0
    sums = 0

    for i in input_str:
        if i > 0 and i % 2 == 0:
            cnt += 1
        sums += i

    print("List: ", input_str)
    print("Odd and positive:", cnt)
    print("Sum: ", sums)
