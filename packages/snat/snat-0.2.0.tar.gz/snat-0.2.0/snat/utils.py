from abc import ABCMeta

from PyQt6 import QtCore, QtWidgets, sip


class ABCQtMeta(sip.wrappertype, ABCMeta):
    """Metaclass for abstract classes using PyQt6."""
    pass


class DotAnimationLabel(QtWidgets.QLabel):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.timer.start(400)

    def update_text(self) -> None:
        text = self.text()
        if text.endswith("..."):
            self.setText(text[:-3])
        else:
            self.setText(text + ".")


class LinkLabel(QtWidgets.QLabel):
    """Label that opens a link when clicked."""

    def __init__(self, text: str | None = None, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setOpenExternalLinks(True)
