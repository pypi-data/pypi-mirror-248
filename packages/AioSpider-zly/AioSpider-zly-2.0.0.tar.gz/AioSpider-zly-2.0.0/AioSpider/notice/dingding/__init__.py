__all__ = [
    'GroupRobot', '__version__', '__author__', '__email__',
    '__publish__', 'set_token', 'set_key_word', 'set_tpl'
]


from typing import Union
from .group_robot import GroupRobot


__version__ = '1.0.0'
__author__ = 'zly'
__email__ = 'zly717216@163.com'
__publish__ = '2022-11-26'


def set_key_word(key_word: Union[str, list] = None):
    GroupRobot.set_key_word(key_word)


def set_tpl(self, tpl: str = None):
    GroupRobot.set_tpl(tpl)

