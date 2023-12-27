from __future__ import annotations

import typing

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from RemoteHotKey.State import State


class UIElement:
    _identifier = ''  # name to identify the button, should be unique
    _label = ''  # the name for ui
    _backgroundColor = '#d0e4fe'  # hex color
    _rowspan = None
    _colspan = None

    def __init__(self, identifier: str, label: str, backgroundColor: str = '#d0e4fe', rowspan=1, colspan=1):
        self._identifier = identifier
        self._label = label
        self._backgroundColor = backgroundColor
        self._rowspan = rowspan
        self._colspan = colspan

    def getIdentifier(self) -> str:
        return self._identifier

    def getLabel(self) -> str:
        return self._label

    def getSize(self) -> typing.Tuple[int, int]:
        return self._rowspan, self._colspan

    def onEvent(self, currentState: State, event: typing.Dict):
        if event.get("identifier") == self._identifier:
            self.updateState(currentState, event)

    def updateState(self, currentState: State, event: typing.Dict) -> None:
        return

    def getUI(self, currentState: State) -> typing.Dict:
        return self._jsonDic()

    def _jsonDic(self) -> typing.Dict:
        jsonDic = {"identifier": self._identifier,
                   "label": self._label,
                   "backgroundColor": self._backgroundColor,
                   "rowspan": self._rowspan,
                   "colspan": self._colspan,
                   "type": "cellui"}
        return jsonDic
