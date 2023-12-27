import enum
import threading
import time
from typing import Tuple

import numpy

from RemoteHotKey.Utility.ActionPerformer import ActionPerformer


class MouseActions(enum.Enum):
    LeftClick = 1
    RightClick = 2
    MoveMouseTo = 3
    MoveMouseBy = 4
    MouseScroll = 5


class KeyboardActions(enum.Enum):
    TapKeyboard = 1
    keyDown = 2
    keyUp = 3


class KeyboardMouseActionPerformer(ActionPerformer):
    downKeys = None
    downKeysLock: threading.Lock

    def __init__(self):
        super().__init__()
        self.downKeys = {}
        self.downKeysLock = threading.Lock()

    def leftClick(self):
        pass

    def rightClick(self):
        pass

    def moveMouseTo(self, x, y):
        pass

    def moveMouseBy(self, dx, dy):
        pass

    def mouseScroll(self, dx, dy):
        pass

    def tapKeyboard(self, key):
        pass

    # Note for keyDown.
    # To avoid issue that:
    # Time 1: keyDown(k, 2)
    # Time 2: keyDown(k, 2)
    # Time 3: No input. The first keyDown is expired, so keyUp(k)
    # Time 4: No input, no any other change. since key `k` is already up.
    # The issue is that I am expecting keyUp(k) called at time 4 and time 3 do nothing.
    # After the fix:
    # Time 1: keyDown(k, 2); downKeys = {k: 1}
    # Time 2: keyDown(k, 2); downKeys = {k: 2}
    # Time 3: No input. downKeys = {k: 1}
    # Time 4: No input. keyUp(k). downKeys = {k: None}
    # The issue is avoided.
    def keyDown(self, key, dur=None):
        with self.downKeysLock:
            if self.downKeys.get(key):
                self.downKeys[key] += 1
            else:
                self.downKeys[key] = 1

        if dur is not None:
            def keyUpAfter():
                time.sleep(dur)
                with self.downKeysLock:
                    count = self.downKeys.get(key)
                    if count is None:
                        return
                    if count == 1:
                        self.keyUp(key)
                    else:
                        self.downKeys[key] = count - 1

            t = threading.Thread(target=keyUpAfter)
            t.daemon = True
            t.start()

    def keyUp(self, key):
        self.downKeys[key] = None

    def print(self, msg):
        print(msg)

    def screenshot(self, monitor: Tuple[int, int, int, int] = None, saveTo=None) -> numpy.ndarray:
        pass
