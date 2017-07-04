from api_objects import *


def catch_exception_decoration(func):
    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except Exception as e:
            return e

    return wrapper


class BaseAPI:
    def __init__(self):
        self.client = CLIENT
        self.jwt = JWT
        self.headers = {
            "Authorization": "Bearer %s" % JWT
        }

    @staticmethod
    def update_default_data(data, **kwargs):
        if kwargs:
            for key in kwargs:
                if key in data.keys():
                    data[key] = kwargs[key]
                else:
                    data[key] = kwargs[key]
        return data
