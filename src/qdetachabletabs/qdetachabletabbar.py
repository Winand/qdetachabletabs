from qtpy.QtCore import Qt, Signal
from qtpy.QtGui import QMouseEvent
from qtpy.QtWidgets import QTabBar, QApplication


class QDetachableTabBar(QTabBar):
    start_dragging = Signal()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        if (event.position() - self.drag_start_position).manhattanLength() \
                                            < QApplication.startDragDistance():
            return
        self.start_dragging.emit()
