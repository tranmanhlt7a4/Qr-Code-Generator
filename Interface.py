from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import qrcode, os

def isEmpty(string : str) -> bool:
    return not string

def cleanUp(platform : str):
    if "demo.png" in os.listdir():
        if "windows" in platform.lower():
            os.system("del demo.png")
        else:
            os.system("rm demo.png")

class Interface(QWidget):
    def __init__(self, platform):
        super().__init__(None)

        self.__platform = platform
        self.__previewZoneSize = QSize(300, 300)

        self.__havePreviewError = False

        self.__contentEditor = QPlainTextEdit(None)
        self.__previewZone = QLabel(None)
        self.__previewZone.setFixedSize(self.__previewZoneSize)

        layoutContent = QHBoxLayout()
        layoutContent.addWidget(self.__contentEditor)
        layoutContent.addWidget(self.__previewZone)

        self.__save = QPushButton("Save")
        self.__save.setIcon(QIcon("./assets/save.png"))

        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(layoutContent)
        mainLayout.addWidget(self.__save)

        self.__save.clicked.connect(self.save)
        self.__contentEditor.textChanged.connect(self.updatePreview)

        self.setWindowIcon(QIcon("./assets/qr-code-generator.png"))
        self.setWindowTitle("QR Code Generator")

    def closeEvent(self, event):
        cleanUp(self.__platform)
        event.accept()

    def resizeEvent(self, event):
        newSize = (self.height() * 60) // 100

        self.__previewZoneSize = QSize(newSize, newSize)
        
        self.__previewZone.setFixedSize(self.__previewZoneSize)
        self.updatePreview()
        event.accept()

    @Slot()
    def save(self):
        # Content mustn't be left empty!
        if isEmpty(self.__contentEditor.toPlainText()):
            QMessageBox.information(self, "Notification", "Nothing to save!")
            return

        # If content not empty
        path = QFileDialog.getSaveFileName(self, "Save QR code image", "", "Images (*.png *.jpg *.svg);; All file (*.*)")
        
        if isEmpty(path[0]):
            return
        else:
            img = qrcode.make(self.__contentEditor.toPlainText())

            try:
                img.save(path[0])
            except Exception:
                QMessageBox.critical(self, "Fatal error", "Can't save this file! Please contact the author for more information!")
                return

            QMessageBox.information(self, "Notification", "File saved!")

    def updatePreview(self):
        if isEmpty(self.__contentEditor.toPlainText()):
            self.__previewZone.setPixmap(QPixmap(""))
        else:
            if not self.__havePreviewError:
                img = qrcode.make(self.__contentEditor.toPlainText())

                try:
                    img.save("demo.png")
                except Exception:
                    QMessageBox.critical(self, "Fatal error", "Can't load preview, your program will not show preview image! Please contact the author for more information!")
                    self.__havePreviewError = True
                    self.__previewZone.setPixmap(QPixmap(""))
                    return

                previewImg = QPixmap("demo.png")
                previewImg = previewImg.scaled(self.__previewZoneSize, Qt.IgnoreAspectRatio)
                self.__previewZone.setPixmap(previewImg)
