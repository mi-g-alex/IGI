import csv
import os.path
import pickle

from CheckDir import CheckDirMixin


class PSuperClass:
    """Просто пример класса для наследования"""
    def __init__(self):
        print("Super Inited")


class Task1(PSuperClass, CheckDirMixin):
    folder = 'Task_1/files/'
    file_csv = folder + "Task_1.csv"
    file_bin = folder + "Task_1.bin"

    class WorkWithCsv:
        """Запись и чтение из csv"""
        def __init__(self, path):
            self.path = path

        def read_all(self):
            with open(self.path, "r+") as f:
                return list(csv.DictReader(f))

        def write_all(self, data):
            with open(self.path, "w+") as f:
                columns = ["name", "old_price", "new_price"]
                writer = csv.DictWriter(f, fieldnames=columns)
                writer.writeheader()
                writer.writerows(data)

        def __str__(self):
            return "csv"

    class WorkWithPickle:
        """Зипись и чтение из бинарника"""
        def __init__(self, path):
            self.path = path

        def read_all(self):
            with open(self.path, "rb+") as f:
                return pickle.load(f)

        def write_all(self, data):
            with open(self.path, 'wb+') as f:
                pickle.dump(data, f)

        def __str__(self):
            return "pickle"

    dict = [
        {"name": "Apple", "old_price": 7, "new_price": 8},
        {"name": "Orange", "old_price": 15, "new_price": 14},
        {"name": "Banana", "old_price": 13, "new_price": 16},
        {"name": "Mango", "old_price": 20, "new_price": 21},
        {"name": "Kiwi", "old_price": 16, "new_price": 15},
        {"name": "Lemon", "old_price": 9, "new_price": 10},
        {"name": "Pineapple", "old_price": 25, "new_price": 29},
        {"name": "Peach", "old_price": 14, "new_price": 13},
        {"name": "Pear", "old_price": 8, "new_price": 9},
        {"name": "Nectarine", "old_price": 11, "new_price": 12},
        {"name": "Lime", "old_price": 999, "new_price": 998},
        {"name": "Fig", "old_price": 123, "new_price": 321},
    ]

    def __init__(self):
        super().__init__()
        print("Task 1. СSV and Pickle")
        super().check_dir(self.folder)
        self.csv_ = self.WorkWithCsv(self.file_csv)
        self.pickle_ = self.WorkWithPickle(self.file_bin)

        self.read_write_dict(self.csv_)
        print()
        self.read_write_dict(self.pickle_)

        self.sort_by_key()

        self.individual_task()

        self.get_info()

    def read_write_dict(self, cls):
        """Вызов функций для чтения \ записи"""
        print()
        print('-' * 100)
        print("Write using", cls.__str__())
        cls.write_all(self.dict)
        print("Read using", cls.__str__())
        self.print_info(cls.read_all())

    def individual_task(self):
        """Найти какие продукты подорожали и насколько"""
        print()
        print('-' * 100)
        new_dict = {i['name']: (i['new_price'] - i['old_price']) / i['old_price'] for i in self.dict if
                    i['old_price'] < i['new_price']}
        for i in new_dict.keys():
            print(f' ↑ {i:<13} - {(new_dict[i] * 100):>7.2f}%')

    @staticmethod
    def print_info(elements):
        """Вывод инфы о продуктах фул"""
        for i in elements:
            print("Name: ", i['name'])
            print("Old price", i['old_price'])
            print("New price", i['new_price'])
            print("Diff: ", float(i['new_price']) - float(i['old_price']))
            print("Diff%: ", (float(i['new_price']) - float(i['old_price'])) / float(i['old_price']) * 100)
            print()
        print('~' * 10)

    def get_info(self):
        """Инфа по названию"""
        while True:
            inp = input("Enter product name or 0 to exit back:  ")
            if inp == "0":
                return
            new_dict = [i for i in self.dict if i['name'].lower() == inp.lower()]
            if len(new_dict) > 0:
                self.print_info(new_dict)
            else:
                print("Product not found")

    def sort_by_key(self):
        """Сортировка по всему что есть только в этой таске"""
        print()
        print('-' * 100)
        print("Unsorted")
        self.print_info(self.dict)

        sorted_by_name = sorted(self.dict, key=lambda x: x['name'])
        print("Sorted by name")
        self.print_info(sorted_by_name)

        sorted_by_old_price = sorted(self.dict, key=lambda x: x['old_price'])
        print("Sorted by old price")
        self.print_info(sorted_by_old_price)

        sorted_by_new_price = sorted(self.dict, key=lambda x: x['new_price'])
        print("Sorted by new price")
        self.print_info(sorted_by_new_price)

        sorted_by_diff = sorted(self.dict, key=lambda x: x['new_price'] - x['old_price'])
        print("Sorted by price difference")
        self.print_info(sorted_by_diff)
