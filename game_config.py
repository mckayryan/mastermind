# mastermind_game config


DEBUG_LEVEL = 1

BOARD_LENGTH = 4
NUM_COLOURS = 6
CORRECT_PLACEMENT = 0
CORRECT_COLOUR = 1
INCORRECT_GUESS = 0

TEST = 'TEST'

SUBMIT_TURN_TYPE = list

def printd(string, level=0, **kwargs):
    if DEBUG_LEVEL >= level:
        print(string.format(**kwargs))

def xstr(_str):
    if _str is None:
        _str = ''
    return str(_str)
