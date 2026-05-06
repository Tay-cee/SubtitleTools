from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Qt App")
        self.setGeometry(100, 100, 600, 400)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        self.label = QLabel("Hello, Qt!")
        self.button = QPushButton("Click me")

        self.button.clicked.connect(self.on_click)

        layout.addWidget(self.label)
        layout.addWidget(self.button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_click(self):
        self.label.setText("Button clicked!")