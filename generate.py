import argparse
import numpy as np
import pickle
from train import Text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, help="путь к файлу, из которого загружается модель.")
    parser.add_argument("--prefix", type=str, action="store",
                        help="необязательный аргумент."
                             "Начало предложения (одно или несколько слов)."
                             "Если не указано, выбирается начальное слово случайно из всех слов")
    parser.add_argument("--length", type=int, help="длина генерируемой последовательности.")
    args = parser.parse_args()
    with open(args.model, "rb") as file:
        model = pickle.load(file)
    model.length = args.length
    model.prefix = args.prefix
    np.random.seed(12082003)
    model.generate()


if __name__ == '__main__':
    main()
