import json

class Configs(object):

    def __init__(self, config_file):
        self.configs = None
        with open(config_file, 'r') as f:
            self.configs = json.load(f)

    def get(self, value):
        return self.configs[value]
