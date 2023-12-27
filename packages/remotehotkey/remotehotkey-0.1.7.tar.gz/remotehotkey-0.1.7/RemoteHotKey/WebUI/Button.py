import typing

from RemoteHotKey.WebUI.UIElement import UIElement
from RemoteHotKey.State import State


class Button(UIElement):
    defaultColor = '#d0e4fe'
    highlightColor = '#99edc3'

    def __init__(self, identifier: str, label: str, rowspan=1, colspan=1):
        super().__init__(identifier, label, rowspan=rowspan, colspan=colspan)
        self._backgroundColor = Button.defaultColor

    def _jsonDic(self) -> typing.Dict:
        jsonDic = super()._jsonDic()
        jsonDic["type"] = "button"
        return jsonDic

    def getUI(self, currentState: State) -> typing.Dict:
        self._backgroundColor = Button.defaultColor
        if currentState.getFromStorage(State.Keys.mostRecentUIElementId) == self._identifier:
            self._backgroundColor = Button.highlightColor

        return self._jsonDic()
