import json
import typing


class OneTimeEvent:
    _name: str
    _timeStamp: float
    _data: typing.Dict
    _handled = False

    def __init__(self, saveData: str=None):
        if saveData is not None:
            saveData = json.loads(saveData)
        else:
            saveData = {}
        self.setFields(saveData.get("name", ""), saveData.get("timeStamp", 0), saveData.get("data", {}))

    def setFields(self, name: str, timeStamp: float, data: typing.Dict):
        self._name = name
        self._timeStamp = timeStamp
        self._data = data

    def getName(self) -> str:
        return self._name

    def getTimeStamp(self) -> float:
        return self._timeStamp

    def getData(self) -> typing.Dict:
        return self._data

    def handle(self):
        self._handled = True

    def isHandled(self) -> bool:
        return self._handled

    def toJSON(self):
        return json.dumps(self.toJSONDic())

    def toJSONDic(self):
        jsonDic = {"name": self._name, "timeStamp": self._timeStamp, "data": self._data.copy()}
        return jsonDic

    def __eq__(self, o: object) -> bool:
        return o.__hash__() == self.__hash__()

    def __hash__(self) -> int:
        return hash(self._name + f"{self._timeStamp}")
