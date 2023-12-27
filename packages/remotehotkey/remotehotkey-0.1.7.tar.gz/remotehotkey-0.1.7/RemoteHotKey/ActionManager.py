from __future__ import annotations

import threading
import time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from RemoteHotKey.State import State


class ActionManager:
    _routineActionRunning = False

    _currentState: State = None
    __routineThread = None

    def __init__(self):
        return

    def __startRoutineAction(self):
        if self.__routineThread is not None:
            return
        self._routineActionStart()

        def run():
            self._routineActionRunning = True
            while self._routineActionRunning:
                self._routineAction()
                time.sleep(0.00001)
            self.__routineThread = None


        self.__routineThread = threading.Thread(target=run)
        self.__routineThread.daemon = True
        self.__routineThread.start()


    def __endRoutineAction(self):
        if self._routineActionRunning:
            self._routineActionEnd()
            self._routineActionRunning = False

    def __startOneTimeAction(self):
        self._oneTimeAction()

    def updateState(self, state: State):
        self._currentState = state

        if self._shouldStartRoutineAction():
            self.__startRoutineAction()
        if self._shouldEndRoutineAction():
            self.__endRoutineAction()
        if self._shouldStartOneTimeAction():
            self.__startOneTimeAction()

    def _shouldStartRoutineAction(self) -> bool:
        return False

    def _shouldEndRoutineAction(self) -> bool:
        return True

    def _shouldStartOneTimeAction(self) -> bool:
        return False

    def _routineActionStart(self):
        return

    def _routineAction(self):
        time.sleep(0.1)
        return

    def _routineActionEnd(self):
        pass

    def _oneTimeAction(self):
        time.sleep(0.01)
        return
