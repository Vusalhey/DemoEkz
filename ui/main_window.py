from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QLineEdit, QLabel, QComboBox, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtGui import QIcon, QPixmap
from db.queries import get_materials  # Функция для загрузки данных из базы
from utils.image_utils import get_pixmap_placeholder  # Утилита для заглушки изображений


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Materials Management")
        self.resize(1000, 700)

        main_layout = QVBoxLayout()

        # поиск, сортировка, и фильтр 
        top_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите для поиска")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Сортировка", "Название", "Тип", "Цена", "Поставщик"])
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Фильтрация", "В наличии", "Нет в наличии"])

        top_layout.addWidget(self.search_input)
        top_layout.addWidget(self.sort_combo)
        top_layout.addWidget(self.filter_combo)

        # Список материалов
        self.materials_list = QListWidget()

        # Пагинация
        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("<")
        self.next_button = QPushButton(">")
        self.page_label = QLabel("1")

        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_button)

        # Сборка основного макета
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.materials_list)
        main_layout.addLayout(pagination_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.prev_button.clicked.connect(self.load_previous_page)
        self.next_button.clicked.connect(self.load_next_page)
        self.search_input.textChanged.connect(self.load_materials)
        self.sort_combo.currentIndexChanged.connect(self.load_materials)
        self.filter_combo.currentIndexChanged.connect(self.load_materials)

        self.current_page = 1
        self.items_per_page = 10
        self.load_materials()

    def load_materials(self):
        try:
            filters = {
                "search": self.search_input.text(),
                "stock": self.filter_combo.currentIndex(),
                "sort_by": self.sort_combo.currentIndex(),
                "page": self.current_page,
                "items_per_page": self.items_per_page,
            }
            materials = get_materials(filters)

            self.materials_list.clear()
            for material in materials:
                item = QListWidgetItem()

                # Подгрузка изображений
                pixmap = QPixmap(material["picture"]) if material["picture"] else get_pixmap_placeholder()
                icon = QIcon(pixmap)

                title = f"{material['title']} | {material['type']}"
                details = f"Минимальное количество: {material['min_quantity']} шт\nПоставщик: {material['supplier']}"
                stock = f"Остаток: {material['stock_quantity']} шт"

                item.setText(f"{title}\n{details}\n{stock}")
                item.setIcon(icon)
                self.materials_list.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def load_previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.page_label.setText(str(self.current_page))
            self.load_materials()

    def load_next_page(self):
        self.current_page += 1
        self.page_label.setText(str(self.current_page))
        self.load_materials()
