from __future__ import annotations

import typing

from RemoteHotKey.WebUI.UIElement import UIElement

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from RemoteHotKey.State import State


class Slider(UIElement):
    _min = 0
    _max = 100
    _value = 0

    def __init__(self, identifier: str, label: str, minV=0, maxV=100, value=0, rowspan=1, colspan=1):
        super().__init__(identifier, label, rowspan=rowspan, colspan=colspan)
        self._min = minV
        self._max = maxV
        self._value = value

    def updateState(self, currentState: State, **kwargs) -> None:
        if "newValue" in kwargs:
            currentState.store(self._identifier, kwargs["newValue"])
        return

    def getUI(self, currentState: State) -> typing.Dict:
        try:
            value = int(currentState.getFromStorage(self._identifier, self._value))
        except ValueError:
            value = self._value

        jsonDic = self._jsonDic()
        jsonDic["type"] = "slider"
        jsonDic["min"] = self._min
        jsonDic["max"] = self._max
        jsonDic["value"] = value

        return jsonDic
