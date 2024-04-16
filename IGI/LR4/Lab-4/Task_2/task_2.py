import re
import zipfile

import CheckDir


class Task2(CheckDir.CheckDirMixin):
    folder = 'Task_2/files'
    file_src = folder + '/src.txt'
    file_ans = folder + '/ans.txt'
    file_zip = folder + '/ans.zip'
    text = ''

    def __init__(self):
        super().check_dir(self.folder)
        print("Task 2. Text")
        self.read_file()
        print("Text\n", self.text)
        self.general_task()
        if not self.read_file():
            return
        self.my_task()

    def read_file(self):
        try:
            with open(self.file_src, 'r') as f:
                self.text = f.read()
                return True
        except Exception as e:
            print("Error:", e)
            return False

    def general_task(self):
        print("Sentence count:", self.find_sentence_count())
        print("Sentence count by type [. ! ?]:", self.find_sentence_type_count())
        print("Average sentence len:", self.find_average_sentence_len())
        print("Average word len:", self.find_average_word_len())
        print("Smile count:", self.find_smiles_count())
        with open(self.file_ans, 'w+') as f:
            f.write(f"Sentence count: {self.find_sentence_count()}\n")
            f.write(f"Sentence count by type [. ! ?]: {self.find_sentence_type_count()}\n")
            f.write(f"Average sentence len: {self.find_average_sentence_len()}\n")
            f.write(f"Average word len: {self.find_average_word_len()}\n")
            f.write(f"Smile count: {self.find_smiles_count()}\n")

    def my_task(self):
        a = self.find_word_with_capital_digit()
        with open(self.file_ans, 'a+') as f:
            print("Print all words that include combination of uppercase letters and numbers:", a)
            f.write(f"Print all words that include combination of uppercase letters and numbers: {a}")
            for i in a:
                print("Is good password " + i, self.check_password_good(i))
                f.write(f"Is good password {i} {self.check_password_good(i)}\n")
            print("Not capital letters words", self.find_not_capital_word_cnt())
            f.write(f"Not capital letters words {self.find_not_capital_word_cnt()}\n")
        with zipfile.ZipFile(self.file_zip, 'w') as zip_file:
            zip_file.write(self.file_ans, arcname=self.file_ans)

    def find_sentence_count(self):
        """Кол-во предложений"""
        return len(re.findall(r'[\.!?]', self.text))

    def find_sentence_type_count(self):
        """Кол-во предложений по типу"""
        sentence_type_list = re.findall(r'[\.!?]', self.text)
        return sentence_type_list.count('.'), sentence_type_list.count('!'), sentence_type_list.count('?')

    def find_average_sentence_len(self):
        """Средняя длина"""
        return sum(len(elem) for elem in re.findall(r'\w+', self.text)) / self.find_sentence_count()

    def find_average_word_len(self):
        """Среднее кол-во букв"""
        lst = re.findall(r'\w+', self.text)
        return sum(len(elem) for elem in lst) / len(lst)

    def find_smiles_count(self):
        """Смайлы"""
        return len(re.findall(r'[:;]-*(\)+|\(+|]+|\[+)', self.text))

    def find_word_with_capital_digit(self):
        """1 большая, 1 цифра"""
        return re.findall(r'\b(?=[A-Za-z0-9]*[A-Z])(?=[A-Za-z0-9]*[0-9])(?=.*)[A-Za-z0-9]{1,}\b', self.text)

    def check_password_good(self, text):
        """Хороший ли пароль"""
        return len(re.findall(r'^(?=[A-Za-z0-9_]*[A-Z])(?=[A-Za-z0-9_]*[0-9])(?=[A-Za-z0-9_]*[a-z])[A-Za-z0-9_]{8,}$',
                              text)) == 1

    def find_not_capital_word_cnt(self):
        """Маленькие слова"""
        return len(re.findall(r'\b(?=[a-z])[a-z]+\b', self.text))
