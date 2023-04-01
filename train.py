import argparse
from collections import Counter
import numpy as np
import os
import pickle
import re
import sys


class Text:

    def __init__(self, input_dir, model):
        self.__input_dir = input_dir
        self.__model = model
        self.__prefix = None
        self.__length = 10
        self.trained_dict = dict()

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
        """
        Функция, которая принимает на вход полный текст файла, а затем обновляет словарь trained_dict.
        В этом словаре ключ - слово, а значение - список слов(с повторениями), которые могут появляться после ключа.

        Args:
            text (str): полный текст файла.

        Returns:
            None.
        """
        # всё, что не русское слово, заменяем на пробел, после преобразуем в список
        text = re.sub('[^а-яё]', ' ', text)
        words = text.split()

        # проходимся по всем словам, кроме последнего;
        # если слова нет в словаре - добавляем его и в значении создаём список из одного последующего слова
        # иначе просто добавляем, рассчитывать вероятность появления слов после какого-то слова будем потом
        for i in range(len(words) - 1):
            if words[i] not in self.trained_dict:
                self.trained_dict[words[i]] = [words[i + 1]]
            else:
                self.trained_dict[words[i]].append(words[i + 1])

    def fit(self):
        """
        Функция, которая обучает нашу модель. Сначала мы инициализируем словарь всевозможных пар слов или из
        файлов указанной папки, или из потока ввода. Затем преобразуем этот словарь так, чтобы значением по ключу
        был список из кортежей, в которых первым элементом идёт возможное слово, а вторым - вероятность его появления.

        Args:
            None.

        Returns:
            None.
        """
        # если папка не указана, то преобразуем текст из потока ввода
        # иначе проходимся по всем файлам указанной папки и обновляем словарь возможных пар слов
        if self.__input_dir is None:
            text = " ".join(list(map(str.strip, sys.stdin.readlines()))).lower()
            self.init_dict(text)
        else:
            for path, dirs, files in os.walk(self.__input_dir):
                for file in files:
                    with open(os.path.join(path, file), 'r', encoding='utf-8') as _:
                        text = _.read().lower()
                        self.init_dict(text)

        # Cчитаем вероятность появления слов:
        # 1) проходимся по всем ключам и значениям словарю;
        # 2) считаем длину списка в значении;
        # 3) из списка делаем словарь подсчетов количества появлений элементов в этом списке;
        # 4) проходимся по созданному Counter-словарю и считаем вероятность каждого слова;
        for key, value in self.trained_dict.items():
            sum_of_words = len(value)
            self.trained_dict[key] = dict(Counter(value))
            lst = list()
            for key1, value1 in self.trained_dict[key].items():
                lst.append((key1, value1 / sum_of_words))
            self.trained_dict[key] = lst

    def generate(self):
        """
        Функция, которая генерирует последовательность слов начиная с префика в заданном количестве слов.
        Если префикс не указан, то слово выбирается случайным образом. Используется в файле generate.py.

        Args:
            None.

        Returns:
            None.
        """
        # настраиваем список слов и слово, с которого начнём генерировать текст
        if self.__prefix is None:
            first_word = str(np.random.choice(list(self.trained_dict.keys()), 1, replace=False)[0])
            words_array = [first_word]
        else:
            first_word = "".join(self.__prefix[-1])
            words_array = self.__prefix.copy()

        # генерируем последовательность слов
        current_word = first_word
        for i in range(self.__length - len(words_array)):
            # список следующих слов
            words_to_choice = [el[0] for el in self.trained_dict[current_word]]
            # список вероятностей следующих слов
            prob = [el[1] for el in self.trained_dict[current_word]]
            next_word = np.random.choice(words_to_choice, 1, p=prob)[0]
            words_array.append(next_word)
            current_word = next_word

        print(" ".join(words_array))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input-dir",
                        action="store",
                        type=str,
                        help="Путь к директории, в которой лежит коллекция документов, по умолчанию stdin")

    parser.add_argument("--model",
                        type=str,
                        help="Путь к файлу, в который сохраняется модель")

    args = parser.parse_args()
    model = Text(args.input_dir, args.model)
    model.fit()
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)


if __name__ == '__main__':
    main()
