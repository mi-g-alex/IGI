import Task_1
import Task_2
import Task_3
import Task_4
import Task_5

if __name__ == "__main__":
    while True:
        a = input("Таsk: ")
        match a:
            case "1":
                task1 = Task_1.Task1()
            case "2":
                task2 = Task_2.Task2()
            case "3":
                task3 = Task_3.Task3()
            case "4":
                task4 = Task_4.Task4()
            case "5":
                task5 = Task_5.Task5()
            case "0":
                exit()

