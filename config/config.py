import json
import logging
import os

from config import CustomObject


class Config(CustomObject):
    LOGGING_LEVEL = {
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }

    def __init__(self, config_file):
        super(CustomObject, self).__init__()
        if 'ROOT' not in os.environ:
            raise RuntimeError('ROOT not set')
        if 'ENV' not in os.environ:
            raise RuntimeError('ENV not set')
        self.root = os.environ['ROOT']
        self.env = os.environ['ENV']
        self.config_file = os.path.join(self.root, config_file)
        self.__load_config()

    def __load_config(self):
        # load JSON config
        with open(self.config_file) as config_file:
            loaded_config = json.load(config_file)
        default_config = loaded_config['production']

        # set develop config
        self.is_develop = not self.env.startswith('prod')
        if self.is_develop and 'develop' in loaded_config:
            self.__copy_config(default_config, loaded_config['develop'], overwrite=True)

        if 'hidden' not in self.config_file:
            default_config['logging']['level'] = self.LOGGING_LEVEL[default_config['logging']['level']]
        self.__set_attrs(self, default_config)

    def __copy_config(self, dest_config, src_config, overwrite=False):
        for key, value in src_config.items():
            if not overwrite and key in dest_config:
                continue
            if type(value) == dict:
                if key not in dest_config:
                    dest_config[key] = {}
                self.__copy_config(dest_config[key], value, overwrite)
            else:
                dest_config[key] = value

    def __set_attrs(self, dest_cls, src_dict):
        for key, value in src_dict.items():
            if type(value) == dict:
                attr_cls = CustomObject()
                self.__set_attrs(attr_cls, src_dict[key])
                setattr(dest_cls, key, attr_cls)
            else:
                setattr(dest_cls, key, value)
