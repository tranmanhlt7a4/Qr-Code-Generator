import sys
from PySide6.QtWidgets import QApplication
import Interface
import platform

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = Interface.Interface(platform.platform())
    window.show()
    
    sys.exit(app.exec())