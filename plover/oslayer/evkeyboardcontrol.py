import sys
import threading
import struct
from collections import namedtuple

import xkeyboardcontrol

FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

TYPE_EV_KEY = 0x01

VALUE_KEY_DOWN = 1
VALUE_KEY_UP = 0

KeyEvent = namedtuple('KeyEvent', 'keystring')

KEY_MAPPING = {30: 'a',
               16: 'q',
               17: 'w',
               31: 's',
               18: 'e',
               32: 'd',
               19: 'r',
               33: 'f',
               46: 'c',
               47: 'v',
               20: 't',
               34: 'g',
               21: 'y',
               35: 'h',
               49: 'n',
               50: 'm',
               22: 'u',
               36: 'j',
               23: 'i',
               37: 'k',
               24: 'o',
               38: 'l',
               25: 'p',
               39: ';',
               26: '[',
               40: '\'',
               2: '1',
               3: '2',
               4: '3',
               5: '4',
               6: '5',
               7: '6',
               8: '7',
               9: '8',
               10: '9',
               11: '0',
               12: '-',
               13: '='}


class KeyboardCapture(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.key_down = lambda x: True
        self.key_up = lambda x: True
        self.src = sys.stdin
        self.mapper = lambda code: KeyEvent(KEY_MAPPING.get(code))

    def run(self):
        event = self.src.read(EVENT_SIZE)
        while event:
            (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)
            if TYPE_EV_KEY == type:
                mapped = self.mapper(code)
                if VALUE_KEY_DOWN == value:
                    self.key_down(mapped)
                elif VALUE_KEY_UP == value:
                    self.key_up(mapped)

            event = self.src.read(EVENT_SIZE)

    def can_suppress_keyboard(self):
        return True

    def suppress_keyboard(self, suppress):
        pass

    def is_keyboard_suppressed(self):
        return True


class KeyboardEmulation(xkeyboardcontrol.KeyboardEmulation):
    pass
