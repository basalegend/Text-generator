# Text-generator
Вступительный экзамен ML/DL Осень'22. N-граммная модель. Генератор текста.

usage: train.py [-h] [--input-dir INPUT_DIR] [--model MODEL]

optional arguments:
  -h, --help            show this help message and exit
  --input-dir INPUT_DIR
                        путь к директории, в которой лежит коллекция документов,по умолчанию stdin
  --model MODEL         путь к файлу, в который сохраняется модель
  
  usage: generate.py [-h] [--model MODEL] [--prefix PREFIX] [--length LENGTH]

optional arguments:
  -h, --help       show this help message and exit
  --model MODEL    путь к файлу, из которого загружается модель.
  --prefix PREFIX  необязательный аргумент.Начало предложения (одно или несколько слов).Если не указано, выбирается
                   начальное слово случайно из всех слов
  --length LENGTH  длина генерируемой последовательности.

train.py генерирует файл model.pkl, в который сохраняется обёрнутая в класс модель. Так как размер моей обученной модели > 100 МБ, то на github её не загрузить
