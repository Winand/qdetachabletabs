from qtpy.QtWidgets import QApplication, QLabel

from qdetachabletabs.qdetachabletabwidget import QDetachableTabWidget

app = QApplication([])

tab_widget = QDetachableTabWidget()
for i in range(1, 5 +1):
    tab_text = f"tabText_{i}"
    tab_name = f"tab {i}"
    tab_widget.addTab(QLabel(tab_text), tab_name)
tab_widget.show()

app.exec()
