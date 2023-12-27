from __future__ import annotations

import threading
import typing
from flask import Flask, Blueprint

from RemoteHotKey.State import State
from RemoteHotKey.FlaskWebUpdateListener import FlaskWebUpdateListener

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from RemoteHotKey.WebUI.UITemplate import UITemplate
    from RemoteHotKey.UpdateListener import UpdateListener
    from RemoteHotKey.ActionManager import ActionManager


class ClientManager:
    _running = False

    _actionManager: typing.List[ActionManager] = None

    _state: State = None
    _ui: UITemplate = None
    _updateListener: UpdateListener = None

    def __init__(self):
        self._actionManager = []
        self._state = State()
        self.app = Flask(__name__)
        self._updateListener = FlaskWebUpdateListener(self)

    def getState(self):
        return self._state

    def onEvent(self, event: typing.Dict):
        self._state.clearEventLog()  # all unhandled event will be ignored when new event come.
        for uiElement in self._ui.getVisibleUIElements():
            uiElement.onEvent(self._state, event)
        self._ui.updateCurrentPageIndex(self._state.getFromStorage(State.Keys.currentPageIndex, 0))

        for actionManager in self._actionManager:
            actionManager.updateState(self._state)

    # return a json contains ui and state
    def toJsonDic(self):
        return {'state': self._state.toJsonDic(), 'ui': self._ui.getCurrentUIPage().getUI(self._state)}

    def setUITemplate(self, uiTemplate: UITemplate):
        self._ui = uiTemplate

    def getUITemplate(self) -> UITemplate:
        return self._ui

    def addActionManager(self, actionManager: ActionManager):
        self._actionManager.append(actionManager)

    def addFlaskBlueprint(self, blueprint: Blueprint):
        self.app.register_blueprint(blueprint)

    def start(self):
        self._running = True
        threading.Thread(target=self.app.run).start()
        self._updateListener.startListening()

    def termination(self):
        self._running = False
