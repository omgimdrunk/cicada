import os
from setuptools import setup, find_packages
import shutil

wheel_objs = ['cicada_d.egg-info', 'build', '__pycache__', 'dist']

mypath = os.path.dirname(os.path.abspath(__file__))
print(mypath)


def cleanup():
    for i in os.listdir(mypath):
        if i in wheel_objs:
            curobj = os.path.join(mypath, i)

            try:
                shutil.rmtree(curobj)
            except PermissionError as PE:
                raise PE
            except FileNotFoundError as NF:
                raise NF
            else:
                pass


class buildCicada(dict):
    def __init__(self):
        super().__init__()
        self['name'] = 'cicada'
        self['version'] = '0.5.10'
        self['description'] = 'sockets lib for cicada'
        self['url'] = 'cicada.network'
        self['author'] = 'knurd.migmo'
        self['author_email'] = 'admin@cicada.network'
        self['license'] = 'DUNODUNCARE'
        self['packages'] = find_packages()
        self['zip_safe'] = False


build = buildCicada()
setup(**build)
