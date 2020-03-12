import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIGS_DIR =  os.path.join(ROOT_DIR, 'configs')


def config_path(config_file):
    return os.path.join(CONFIGS_DIR, config_file)
