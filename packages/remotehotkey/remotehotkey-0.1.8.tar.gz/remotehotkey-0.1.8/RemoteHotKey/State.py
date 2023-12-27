import json
from typing import List, Dict

from RemoteHotKey.OneTimeEvent import OneTimeEvent


class State:
    class Keys:
        currentPageIndex: str = "State.Keys.currentPageIndex"
        mostRecentUIElementId: str = "State.Keys.mostRecentUIElementId"

    MaxLenOfEventLog = 10

    _eventLog: List[OneTimeEvent] = None
    _storage: Dict = None

    def __init__(self, jsonData=None, numberOfStates: int = 20):
        self._numberOfStates = numberOfStates
        self._states = [0] * numberOfStates

        self._eventLog = []

        self._storage = {}
        self.store(State.Keys.currentPageIndex, 0)

        if jsonData is not None:
            self.__loadFromJson(jsonData)

    def store(self, key: str, value):
        self._storage[key] = value

    def getFromStorage(self, key: str, default=None):
        if self._storage.get(key) is not None:
            return self._storage.get(key)
        return default

    def getStorage(self):
        return self._storage

    def __loadFromJson(self, jsonData):
        loadData = json.loads(jsonData)
        self._storage = loadData['storage']
        for event in loadData['eventLog']:
            self._eventLog.append(OneTimeEvent(json.dumps(event)))

    def getEventLog(self) -> List[OneTimeEvent]:
        return self._eventLog

    def addOneTimeEvent(self, oneTimeEvent: OneTimeEvent):
        self._eventLog.append(oneTimeEvent)
        if len(self._eventLog) > self.MaxLenOfEventLog:
            self._eventLog.pop(0)

    def toJsonDic(self):
        return {"storage": self._storage, "eventLog": [x.toJSONDic() for x in self._eventLog]}

    def clearHandledEvents(self):
        self._eventLog = [x for x in self._eventLog if not x.isHandled()]

    def clearEventLog(self):
        self._eventLog = []

    def clearStorage(self):
        self._storage = {}
