import argparse
from collections import Counter
import numpy as np
import os
import pickle
import re
import sys


class Text:

    def __init__(self, path, model):
        self.__prefix = None
        self.__length = 10
        self.__input_dir = path
        self.__model = model
        self.trained_dict = dict()

    """Декораторы, чтобы в generate.py обратиться к length и prefix"""

    @property
    def prefix(self):
        return self.__prefix

    @prefix.setter
    def prefix(self, words):
        if words is not None:
            self.__prefix = words.split()

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, val):
        self.__length = val

    def init_dict(self, text):
        text = re.sub('[^а-яё]', ' ', text)  # всё, что не русское слово, заменяем на пробел
        words = text.split()  # создаём список слов
        for i in range(len(words) - 1):
            if words[i] not in self.trained_dict:  # если слова нет среди ключей словаря
                self.trained_dict[words[i]] = [words[i + 1]]  # создаём список из одного слова
            else:  # иначе просто добавляем, рассчитывать вероятность будем потом
                self.trained_dict[words[i]].append(words[i + 1])

    def fit(self):
        if self.__input_dir is None:
            text = " ".join(list(map(str.strip, sys.stdin.readlines()))).lower()
            self.init_dict(text)
        else:
            for path, dirs, files in os.walk(self.__input_dir):
                for file in files:
                    with open(os.path.join(path, file), 'r', encoding='utf-8') as _:
                        text = _.read().lower()
                        self.init_dict(text)

        for key, value in self.trained_dict.items():  # проходимся по всему словарю, чтобы посчитать вероятность
            sum_of_words = len(value)  # количество слов в списке - n в формуле вероятности p = k / n
            self.trained_dict[key] = dict(Counter(value))  # считаем количество слов в списке и делаем словарь
            lst = list()  # промежуточный список, который потом станет значением ключа
            for key1, value1 in self.trained_dict[key].items():  # проходимся по созданному Counter-словарю
                lst.append((key1, value1 / sum_of_words))
            self.trained_dict[key] = lst  # считаем вероятность следующего слова по формуле вероятности p = k / n

    def generate(self):
        if self.__prefix is None:
            first_word = "".join(np.random.choice(list(self.trained_dict.keys()), 1, replace=False))
            words_array = [first_word]
        else:
            first_word = "".join(self.__prefix[-1])
            words_array = self.__prefix.copy()
        current_word = first_word
        for i in range(self.__length - len(words_array)):
            arr = [el[0] for el in self.trained_dict[current_word]]  # список следующих слов
            prob = [el[1] for el in self.trained_dict[current_word]]  # список вероятностей следующих слов
            next_word = "".join(np.random.choice(arr, 1, p=prob))
            words_array.append(next_word)
            current_word = "".join(next_word)

        print(" ".join(words_array))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", action="store", type=str,
                        help="путь к директории, в которой лежит коллекция документов,"
                             "по умолчанию stdin")
    parser.add_argument("--model", type=str, help="путь к файлу, в который сохраняется модель")
    args = parser.parse_args()
    model = Text(args.input_dir, args.model)
    model.fit()
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)


if __name__ == '__main__':
    main()
