

from os import stat


class Metadata:

    def __init__(self):
        self.__data = {}

    def get_value(self, field_name):
        if(field_name in self.__data):
            return self.__data[field_name]
        else:
            return None

    def set_value(self, field_name, value):
        self.__data[field_name] = value

    @staticmethod
    def from_string(string):
        entries = string.split("\n")[:-1]
        data = {x[0]: x[1] for x in (y.split(": ") for y in entries)}
        metadata = Metadata()
        metadata.__data = data
        return metadata

    def __str__(self) -> str:
        data = ""
        print(self.__data)
        for key, value in self.__data.items():
            data += "{}: {}\n".format(key, value)
        return data