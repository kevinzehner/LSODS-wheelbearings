import sys
from PySide6.QtWidgets import QApplication
from src.create_indexes import create_indexes
from src.window import Window, DB_PATH, ASSETS


def execute():
    # Create indexes (if they don't exist)

    create_indexes(DB_PATH)

    # Start the application
    app = QApplication(sys.argv)

    # Apply the stylesheet
    try:
        with open(ASSETS / "style.qss", "r") as style_file:
            app.setStyleSheet(style_file.read())
    except Exception as e:
        print(f"Error loading stylesheet: {e}")

    window = Window()
    window.show()
    window.showMaximized()
    sys.exit(app.exec())
