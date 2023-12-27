from __future__ import annotations

import json
import logging
import os.path
import time

from flask import request, render_template, Blueprint

from RemoteHotKey.UpdateListener import UpdateListener
from RemoteHotKey.definitions import ROOT_DIR


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from RemoteHotKey.ClientManager import ClientManager


class FlaskWebUpdateListener(UpdateListener):
    _clientManager = None

    def __init__(self, clientManager: ClientManager):
        super().__init__()

        self._clientManager = clientManager

        self.blueprint = Blueprint("FlaskWebUpdateListener", __name__, url_prefix="/",
                                   template_folder=os.path.join(ROOT_DIR, "WebUI/templates"))
        self.configure_routes()

    def configure_routes(self):
        self.blueprint.add_url_rule('/uiUpdate', 'uiUpdate', self.uiUpdate, methods=['POST'])
        self.blueprint.add_url_rule('/', 'index', self.mainUI)

    def mainUI(self):
        return render_template("controlpadFlask.html")

    def uiUpdate(self):
        self.onEvent(jsonStr=request.get_data())
        return json.dumps(self._clientManager.toJsonDic()['ui'])

    def startListening(self):
        self._clientManager.addFlaskBlueprint(self.blueprint)

    def onEvent(self, jsonStr):
        jsonData = json.loads(jsonStr)
        timeReceived = 0

        for event in [jsonData]:
            if event.get("name") == "event" and event.get("data"):
                self._clientManager.onEvent(event.get("data"))
                try:
                    timeReceived = int(event.get("data").get("time"))
                except ValueError:
                    pass
            elif event.get("name") in ["requestUiUpdate", "uiUpdate"]:
                pass

        logging.info(f"Latency: {int(time.time() * 1000) - timeReceived} ms; data: {jsonStr}")
        return
