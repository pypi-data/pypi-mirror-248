# import typing
#
# from RemoteHotKey.State import State
# from RemoteHotKey.WebUI.Button import Button
# from typing import Callable, Any
#
#
# class GenericButton(Button):
#     _defaultUpdateState: Callable[[State, Any], None] = None
#     _defaultGetUI: Callable[[State], typing.Dict] = None
#
#     def __init__(self, identifier: str, label: str):
#         super().__init__(identifier, label)
#
#         self._defaultUpdateState = super().updateState
#         self._defaultGetUI = super().getUI
#
#     def setUpdateState(self, func: Callable[[State, Any], None]):
#         self._defaultUpdateState = func
#
#     def setGetUI(self, func: Callable[[State], typing.Dict]):
#         self._defaultGetUI = func
#
#     def updateState(self, currentState: State, **kwargs) -> None:
#         return self._defaultUpdateState(currentState, **kwargs)
#
#     def getUI(self, currentState: State) -> typing.Dict:
#         return self._defaultGetUI(currentState)
