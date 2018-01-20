import os

class Load():
    """
    Load each payloads file for directory and charge it one time in RAM to prevent too much read action
    """

    def __init__(self, path):
        self.path = os.path.dirname(os.path.realpath(path)) + "/payloads/"
        self.files = os.listdir(self.path)

    def __call__(self, *args, **kwargs):
        return {file_name:open(self.path + file_name, "r").read() for file_name in self.files}