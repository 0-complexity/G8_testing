import uuid, random, os

class Utils:
    def __init__(self):
        pass

    def random_string(self, length=10):
        return str(uuid.uuid4()).replace('-', '')[0:length]
