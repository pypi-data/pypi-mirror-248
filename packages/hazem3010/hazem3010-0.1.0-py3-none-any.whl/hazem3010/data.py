import json
import threading
from json import JSONDecodeError


class Data:
    lock = threading.Lock()

    def __init__(self, file_name: str):
        self.__file_name__ = file_name
        try:
            self.__data__ = json.load(open(file_name, 'r', encoding='utf-8'))
        except (FileNotFoundError, JSONDecodeError):
            self.__data__ = {}

    def __call__(self, key, from_list: list = None, loop: bool = False):
        return self.get(key, from_list, loop)

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        Data.lock.acquire()
        self.__data__[key] = value
        json.dump(self.__data__, open(self.__file_name__, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
        Data.lock.release()

    def get(self, key, from_list: list = None, loop: bool = False):
        if key not in self.__data__.keys():
            self.__data__[key] = 0
        if isinstance(self.__data__[key], int):
            Data.lock.acquire()
            self.__data__[key] += 1
            json.dump(self.__data__, open(self.__file_name__, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
            Data.lock.release()
            try:
                return self.__data__[key] - 1 if from_list is None else from_list[self.__data__[key] - 1]
            except IndexError as IE:
                if loop:
                    self.reset(key)
                    if len(from_list) > 0:
                        return self.get(key, from_list, loop)
                    else:
                        raise IndexError("The list is empty")
                else:
                    raise IE
        else:
            return self.__data__[key]

    def reset(self, key):
        self.__data__[key] = 0
        Data.lock.acquire()
        json.dump(self.__data__, open(self.__file_name__, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
        Data.lock.release()
