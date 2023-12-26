from PyQt5.QtWidgets import *

from python_orders.domain.value_objects.order_item import OrderItem


class DetailsWindow(QDialog):
    def __init__(self, items: list[OrderItem], parent=None):
        super().__init__(parent)

        self.setWindowTitle("Детали заказа")
        self.setGeometry(300, 300, 600, 400)

        # Строка поиcка
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Поиск товаров...")
        self.searchBar.textChanged.connect(self.search_item)

        # Создание таблицы для отображения деталей товаров
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Название", "Цена", "Количество"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.load_items(items)

        # Установка макета
        layout = QVBoxLayout()
        layout.addWidget(self.searchBar)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def search_item(self, text):
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            self.table.setRowHidden(
                row, text.lower() not in item.text().lower() if item else False
            )

    def load_items(self, items: list[OrderItem]):
        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(item.name))
            self.table.setItem(row, 1, QTableWidgetItem(str(item.price)))
            self.table.setItem(row, 2, QTableWidgetItem(str(item.quantity)))
