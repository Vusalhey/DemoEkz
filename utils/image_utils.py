from PyQt5.QtGui import QPixmap

def get_pixmap_placeholder():
    pixmap = QPixmap(50, 50)
    pixmap.fill()
    return pixmap
