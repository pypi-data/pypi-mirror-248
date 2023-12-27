from RemoteHotKey.WebUI.UIElement import UIElement
import typing
from RemoteHotKey.State import State


class UIPageFullException(Exception):
    pass


class UIPage:
    _pageSize: typing.Tuple[int, int]
    _viewSize: typing.Tuple[int, int]

    _uiElements: typing.List[typing.List[typing.Optional[UIElement]]] = None

    PlaceHolder = UIElement("UIElement.PlaceHolder", "", rowspan=-1, colspan=-1)
    EmptyCell = UIElement("UIElement.EmptyCell", "", rowspan=1, colspan=1)

    def __init__(self, pageSize: typing.Tuple[int, int], viewSize: typing.Tuple[int, int] = None):

        self._pageSize = pageSize
        if viewSize is not None:
            self._viewSize = viewSize
        else:
            self._viewSize = pageSize

        self._uiElements = [[None for _ in range(pageSize[1])] for _ in range(pageSize[0])]

    def _canAddUIElementTo(self, uiElement: UIElement, row: int, column: int) -> bool:
        for i in range(uiElement.getSize()[0]):
            for j in range(uiElement.getSize()[1]):
                try:
                    cell = self._uiElements[row + i][column + j]
                except IndexError:
                    return False

                if cell is not None:
                    return False
        return True

    def _addUIElementTo(self, uiElement: UIElement, row: int, column: int):
        for i in range(uiElement.getSize()[0]):
            for j in range(uiElement.getSize()[1]):
                self._uiElements[row + i][column + j] = UIPage.PlaceHolder
        self._uiElements[row][column] = uiElement
        return

    def addUIElement(self, uiElement: UIElement, row: int = None, column: int = None):
        if (row is not None) and (column is not None):
            if self._canAddUIElementTo(uiElement, row, column):
                self._addUIElementTo(uiElement, row, column)
                return
            else:
                raise UIPageFullException()
        else:
            for i in range(self._pageSize[0]):
                for j in range(self._pageSize[1]):
                    if self._canAddUIElementTo(uiElement, i, j):
                        return self.addUIElement(uiElement, i, j)
        raise UIPageFullException()

    def getUIElements(self) -> typing.List[typing.Optional[UIElement]]:
        ret = []
        for i in self._uiElements:
            ret += [x for x in i if x is not None]
        return ret

    def getSize(self):
        return self._pageSize

    def getUI(self, currentState: State) -> typing.Dict:
        uis = []
        for i in range(self._pageSize[0]):
            for j in range(self._pageSize[1]):
                ele = self._uiElements[i][j]
                if ele is None:
                    ele = UIPage.EmptyCell
                uis.append({"row": i, "col": j, "data": ele.getUI(currentState)})
        return {"pageSize": {"rows": self._pageSize[0], "cols": self._pageSize[1]},
                "viewSize": {"rows": self._viewSize[0], "cols": self._viewSize[1]},
                "ui": uis}


class UITemplate:
    @staticmethod
    def nextPage(state: State):
        state.store(State.Keys.currentPageIndex, state.getFromStorage(State.Keys.currentPageIndex, 0) + 1)

    @staticmethod
    def previousPage(state: State):
        state.store(State.Keys.currentPageIndex, state.getFromStorage(State.Keys.currentPageIndex, 0) - 1)

    @staticmethod
    def firstPage(state: State):
        state.store(State.Keys.currentPageIndex, 0)

    @staticmethod
    def setPageIndexTo(state: State, index):
        state.store(State.Keys.currentPageIndex, index)

    _name: str = None
    _currentPageIndex = 0
    _uiPages: typing.List[UIPage] = None

    def __init__(self, name: str):
        self._name = name
        self._uiPages = []

    def getName(self) -> str:
        return self._name

    def addPage(self, page: UIPage):
        self._uiPages.append(page)

    def getCurrentPageIndex(self):
        return self._currentPageIndex

    def getUIPages(self):
        return self._uiPages

    def getCurrentUIPage(self) -> UIPage:
        return self._uiPages[self._currentPageIndex]

    def updateCurrentPageIndex(self, index: int):
        self._currentPageIndex = index % len(self._uiPages)

    def getVisibleUIElements(self) -> typing.List[UIElement]:
        return self.getCurrentUIPage().getUIElements()

    def getInvisibleUIElements(self) -> typing.List[UIElement]:
        buttons = []
        for i in range(len(self._uiPages)):
            if i != self._currentPageIndex:
                buttons += self._uiPages[i].getUIElements()

        return buttons

    def getAllUIElements(self) -> typing.List[UIElement]:
        buttons = self.getVisibleUIElements()
        for b in self.getInvisibleUIElements():
            if b not in buttons:
                buttons.append(b)
        return buttons
