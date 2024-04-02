import Tasks


def main():
    tmp = input("Select task (1-5): ")
    match tmp:
        case "1":
            Tasks.task_1()
        case "2":
            Tasks.task_2()
        case "3":
            Tasks.task_3()
        case "4":
            Tasks.task_4()
        case "5":
            Tasks.task_5()
        case "0":
            exit()
    main()


if __name__ == "__main__":
    main()
