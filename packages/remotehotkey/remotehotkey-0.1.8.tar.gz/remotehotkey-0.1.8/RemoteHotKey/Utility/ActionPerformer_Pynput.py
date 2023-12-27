from typing import Tuple

import pynput
import numpy
import mss
import cv2

from RemoteHotKey.Utility.KeyboardMouseActionPerformer import KeyboardMouseActionPerformer


class ActionPerformer_Pynput(KeyboardMouseActionPerformer):
    _keyboardController = None
    _mouseController = None

    def __init__(self,
                 keyboardController: pynput.keyboard.Controller = pynput.keyboard.Controller(),
                 mouseController: pynput.mouse.Controller = pynput.mouse.Controller()):
        super().__init__()
        self._keyboardController = keyboardController
        self._mouseController = mouseController

    def leftClick(self):
        self._mouseController.click(pynput.mouse.Button.left)

    def rightClick(self):
        self._mouseController.click(pynput.mouse.Button.right)

    def moveMouseTo(self, x, y):
        self._mouseController.position = (x, y)

    def moveMouseBy(self, dx, dy):
        self._mouseController.move(dx, dy)

    def mouseScroll(self, dx, dy):
        self._mouseController.scroll(dx, dy)

    def tapKeyboard(self, key):
        self._keyboardController.tap(key)

    def keyDown(self, key, dur=None):
        super().keyDown(key, dur)

        if self.downKeys[key] == 1:
            self._keyboardController.press(key)

    def keyUp(self, key):
        super().keyUp(key)
        self._keyboardController.release(key)

    def print(self, msg):
        print(msg)

    # monitor : (x, y, end x, end y)
    def screenshot(self, monitor: Tuple[int, int, int, int] = None, saveTo=None) -> numpy.ndarray:
        with mss.mss() as sct:
            if not monitor:
                monitor = sct.monitors[1]
            img = sct.grab(monitor)
        if saveTo:
            cv2.imwrite(saveTo, img)
        return numpy.array(img)
