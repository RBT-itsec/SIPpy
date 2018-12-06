"""
Minimal Linux Terminal Colors -- subpart of colorama: https://github.com/tartley/colorama
"""

CSI = '\033['
OSC = '\033]'
BEL = '\007'


def code_to_chars(code):
    """ Return char representing code """
    return CSI + str(code) + 'm'


def set_title(title):
    """ Set title """
    return OSC + '2;' + title + BEL


def clear_screen(mode=2):
    """ Clear screen """
    return CSI + str(mode) + 'J'


def clear_line(mode=2):
    """ Clear line """
    return CSI + str(mode) + 'K'


class AnsiCodes(object):
    """ Ansi Codes """

    def __init__(self):
        """ Init """
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))


class AnsiFore(AnsiCodes):
    """ Foreground colors """
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39


class AnsiBack(AnsiCodes):
    """ Background colors """
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    RESET = 49


Fore = AnsiFore()
Back = AnsiBack()
