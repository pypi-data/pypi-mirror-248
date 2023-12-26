import asyncio
from functools import partial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from python_orders.application.get_orders.use_case import GetOrders
from python_orders.domain.models.order import Order
from python_orders.presentation.qt.win_to_show_items import DetailsWindow


class TableWindow(QMainWindow):
    def __init__(self, get_orders: GetOrders):
        super().__init__()
        self.__get_orders = get_orders

        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создание календаря
        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.data_filter)

        # Создание таблицы
        self.table = QTableWidget()
        self.table.setColumnCount(100)

        # Размещение календаря и таблицы в вертикальном макете
        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.table)
        central_widget.setLayout(layout)

        # Настройка размера окна
        self.setGeometry(300, 300, 600, 400)
        self.setMinimumSize(770, 400)
        self.setWindowTitle("Просмотр данных")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_server)
        self.timer.start(2000)

    def data_filter(self):
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        for row in range(self.table.rowCount()):
            date_item = self.table.item(row, 4)
            if date_item and selected_date in date_item.text():
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def start_server(self):
        orders = asyncio.new_event_loop().run_until_complete(
            self.__get_orders(None),
        )
        print(orders)
        self.update_table(orders)

    def update_table(self, orders: list[Order]):
        self.table.clear()
        self.table.setRowCount(len(orders))
        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels(
            ["Email", "Общая стоимость", "Подробнее", "ID заказа", "Дата", "Время"]
        )

        for row, order in enumerate(orders):
            email_item = QTableWidgetItem(order.user_email)
            email_item.setFlags(email_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, email_item)

            total_cost_item = QTableWidgetItem(
                str(sum(item.price * item.quantity for item in order.items))
            )
            total_cost_item.setFlags(total_cost_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, total_cost_item)

            order_id_item = QTableWidgetItem(str(order.id))
            order_id_item.setFlags(order_id_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 3, order_id_item)

            order_date_item = QTableWidgetItem(
                order.created_at.isoformat().split("T")[0]
            )
            order_date_item.setFlags(order_date_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 4, order_date_item)

            order_time_item = QTableWidgetItem(
                order.created_at.isoformat().split("T")[1].split(".")[0]
            )
            order_time_item.setFlags(order_time_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 5, order_time_item)

            details_button = QPushButton("Подробнее")

            details_button.clicked.connect(
                partial(
                    lambda order: self.show_purchase_details(order.items),
                    order=order,
                )
            )
            self.table.setCellWidget(row, 2, details_button)

        self.data_filter()

        # email_item = QTableWidgetItem(order.user_email)
        # email_item.setFlags(email_item.flags() & ~Qt.ItemIsEditable)
        # self.table.setItem(0, 0, email_item)
        #
        # total_cost_item = QTableWidgetItem(
        #     str(sum(item.price * item.quantity for item in order.items))
        # )
        # total_cost_item.setFlags(total_cost_item.flags() & ~Qt.ItemIsEditable)
        # self.table.setItem(0, 1, total_cost_item)
        #
        # order_id_item = QTableWidgetItem(order.id)
        # order_id_item.setFlags(order_id_item.flags() & ~Qt.ItemIsEditable)
        # self.table.setItem(0, 3, order_id_item)

        # re_order_date_item = QTableWidgetItem(order.date.split("T")[0])
        # re_order_date_item.setFlags(re_order_date_item.flags() & ~Qt.ItemIsEditable)
        # self.table.setItem(0, 4, re_order_date_item)
        #
        # re_order_time_item = QTableWidgetItem(order.date.split("T")[1].split(".")[0])
        # re_order_time_item.setFlags(re_order_time_item.flags() & ~Qt.ItemIsEditable)
        # self.table.setItem(0, 5, re_order_time_item)

        # details_button = QPushButton("Подробнее")
        # details_button.clicked.connect(lambda: self.show_purchase_details(order.items))
        # self.table.setCellWidget(0, 2, details_button)

    def show_purchase_details(self, items):
        details_window = DetailsWindow(items, self)
        details_window.exec_()

    def closeEvent(self, event):
        self.server_thread.stop_server()
        self.server_thread.join()
        super().closeEvent(event)
