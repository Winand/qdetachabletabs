from typing import TypedDict

from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from qtpy.QtCore import QMimeData, Qt
from qtpy.QtGui import QDrag
from qtpy.QtWidgets import QTabWidget, QWidget

from qdetachabletabs.qdetachabletabbar import QDetachableTabBar
from qdetachabletabs.utils import some


class TabInfo(TypedDict):
    name: str
    widget: QWidget

msi_mimetype = "application/x-tabwidget.index"


class QDetachableTabWidget(QTabWidget):
    drag_info: dict[int, TabInfo] = {}
    key_value = 0

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.resize(640, 480)
        new_tabbar = QDetachableTabBar(self)
        new_tabbar.start_dragging.connect(self.start_dragging)
        self.setTabBar(new_tabbar)
        self.setAcceptDrops(True)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.currentChanged.connect(lambda idx: idx == -1 and self.close())
        self.setTabsClosable(True)

        def _tabCloseRequested(idx: int):
            self.removeTab(idx)
            if self.count() == 0:
                self.close()
        self.tabCloseRequested.connect(_tabCloseRequested)

    def start_dragging(self):
        drag = QDrag(self)
        mime_data = QMimeData()
        QDetachableTabWidget.key_value += 1
        key = QDetachableTabWidget.key_value
        self.drag_info[key] = TabInfo(
            name=some(self.tabBar()).tabText(self.currentIndex()),
            widget=some(self.currentWidget())
        )
        mime_data.setData(msi_mimetype, str(key).encode())
        pixmap = some(self.currentWidget()).grab()
        drag.setMimeData(mime_data)
        drag.setPixmap(pixmap)
        action = drag.exec(Qt.DropAction.CopyAction | Qt.DropAction.MoveAction)
        if action == Qt.DropAction.IgnoreAction:
            if self.count() == 1:
                return
            tab_widget = QDetachableTabWidget()
            tab_widget.addTab(self.currentWidget(), self.tabText(self.currentIndex()))
            tab_widget.show()

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if some(event.mimeData()).hasFormat(msi_mimetype):
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        key = some(event.mimeData()).data(msi_mimetype).toInt()[0]
        if not (info := self.drag_info.pop(key, None)):
            return
        idx = some(self.tabBar()).tabAt(event.position().toPoint())
        if 0 <= idx < self.count():
            self.insertTab(idx, info["widget"], info["name"])
            self.setCurrentIndex(idx)
        else:
            self.addTab(info["widget"], info["name"])
            self.setCurrentIndex(self.count() - 1)
        event.acceptProposedAction()
