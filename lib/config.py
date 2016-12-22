from os.path import join, dirname
import yaml


def config_from_yaml():
    """
    Reads yaml config and returns
    a dictionary.
    """
    DIR = dirname(__file__)
    with open(join(DIR, '..', 'config.yaml')) as f:
        y = yaml.load(f.read())
    return y
