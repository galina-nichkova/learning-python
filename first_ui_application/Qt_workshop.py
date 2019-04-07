import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtCharts import QtCharts
from PySide2.QtGui import *

class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.items = 0

        # Example data
        self._data = {"Water": 24.5, "Electricity": 55.1, "Rent": 850.0,
                      "Supermarket": 230.4, "Internet": 29.99, "Spätkauf": 21.85,
                      "BVG Ticket": 60.0, "Coffee": 22.45, "Meetup": 0.0}

        # Left
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Description", "Quantity"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Right
        self.description = QLineEdit()
        self.quantity = QLineEdit()
        self.add = QPushButton("Add")
        self.clear = QPushButton("Clear")
        self.quit = QPushButton("Quit")
        self.plot = QPushButton("Plot")

        # Chart
        self.chart_view = QtCharts.QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.right = QVBoxLayout()
        self.right.setMargin(10)
        self.right.addWidget(QLabel("Description"))
        self.right.addWidget(self.description)
        self.right.addWidget(QLabel("Quantity"))
        self.right.addWidget(self.quantity)
        self.right.addWidget(self.add)
        self.right.addWidget(self.plot)
        self.right.addWidget(self.chart_view)
        self.right.addWidget(self.clear)
        self.right.addWidget(self.quit)

        # Disable the "Add" button
        self.add.setEnabled(False)

        # Layout
        self.layout = QHBoxLayout()

        #self.table_view.setSizePolicy(size)
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.right)

        self.setLayout(self.layout)

        self.fill_data()

        # Add action
        self.add.clicked.connect(self.add_data)

        # Quit action
        self.quit.clicked.connect(self.quit_app)

        # Clear table action
        self.clear.clicked.connect(self.clear_table)

        # Check that "Quantity" and "Description" are not empty
        self.quantity.textChanged.connect(self.check_if_text_added)
        self.description.textChanged.connect(self.check_if_text_added)

        # Add chart
        self.plot.clicked.connect(self.add_chart)

    def fill_data(self, data=None):
        data = self._data if not data else data
        for key, value in data.items():
            self.table.insertRow(self.items)
            self.table.setItem(self.items ,0 ,QTableWidgetItem(key))
            self.table.setItem(self.items ,1 ,QTableWidgetItem(str(value)))
            self.items += 1

    @Slot()
    #accept text from the 2 QLineEdit-s and insert it into the QTableWidget when Add button is pushed
    def add_data(self, desc=None, quan=None):
        desc = self.description.text() if not desc else desc
        print(desc)
        quan = self.quantity.text() if not quan else quan
        print(quan)
        self.table.insertRow(self.items)
        self.table.setItem(self.items, 0, QTableWidgetItem(desc))
        self.table.setItem(self.items, 1, QTableWidgetItem(quan))
        self.items += 1

    @Slot()
    def quit_app(self, checked):
        QApplication.quit()

    @Slot()
    def clear_table(self):
        self.table.setRowCount(0)
        self.items = 0

    @Slot()
    def check_if_text_added(self):
        if self.quantity.text() and self.description.text():
            self.add.setEnabled(True)
        else:
            self.add.setEnabled(False)

    @Slot()
    def add_chart(self):
        self.pie = QtCharts.QPieSeries()
        items_temp = self.items
        while self.items > 0:
            self.pie.append(self.table.item(self.items-1, 0).text(), float(self.table.item(self.items-1, 1).text()))
            self.items -= 1
        self.items = items_temp
        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.pie)
        self.chart_view.setChart(self.chart)

class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Tutorial")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(exit_action)

        # Widget
        self.setCentralWidget(widget)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)

    #Widget
    widget = MainWidget()

    # Window
    window = MainWindow(widget)
    window.resize(600,800)
    window.show()
    sys.exit(app.exec_())

