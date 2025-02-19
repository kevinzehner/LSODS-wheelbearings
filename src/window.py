import os
import sys
from pathlib import Path
import src.database as database
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src import images

if hasattr(sys, "frozen"):
    PARENT = Path(sys.executable).parent
    APPDIR = Path(__file__).parent.parent
else:
    PARENT = Path(__file__).parent.parent
    APPDIR = PARENT

ASSETS = APPDIR / "assets"
DB_PATH = APPDIR / "wheelbearings_LSODS.db"


class ComboWidget(QWidget):

    currentTextChanged = Signal(str)

    def __init__(self, label, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(50)
        self.label = QLabel(label)
        self.setProperty("class", "ComboWidget")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.label_widget = QWidget(self)
        self.label_widget.setProperty("class", "LabelWidget")
        self.label_layout = QVBoxLayout(self.label_widget)
        self.label_layout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.combo = QComboBox()
        self.combo.setFixedSize(250, 50)
        self.hlayout = QHBoxLayout(self)
        self.hlayout.addWidget(self.label_widget)
        self.hlayout.addWidget(self.combo)
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.combo.currentTextChanged.connect(self.currentTextChanged.emit)

    def addItem(self, item):
        self.combo.addItem(item)

    def addItems(self, items):
        self.combo.addItems(items)

    def currentText(self):
        return self.combo.currentText()

    def clear(self):
        self.combo.clear()


class LeftSide(QWidget):

    displayResults = Signal(list)
    clearResults = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        scroll_area_layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumWidth(800)

        content_widget = QWidget()
        self.scroll_area.setWidget(content_widget)

        scroll_area_layout.addWidget(self.scroll_area)

        layout = QVBoxLayout(content_widget)

        self.footer = QLabel(
            "+86-19584855673\n"
            "autoparts@lsods.com\n"
            "No. 313-319, Building 18, Kailong,\n"
            "International Auto Parts City, Baiyun District, Guangzhou"
        )
        self.footer.setProperty("class", "footer")

        self.logolabel = QLabel()
        self.logolabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.logolabel.setPixmap(
            QPixmap(":new-logo.PNG").scaledToHeight(
                120, Qt.TransformationMode.SmoothTransformation
            )
        )
        self.logolabel.setProperty("class", "Logo")

        self.instructions_label = QLabel()
        self.instructions_label.setText(
            "<html><body><p>Please select the manufacturer, model, engine size, mark series,<br>"
            "drive type, and position to search for wheel bearings.</p></body></html>"
        )
        self.instructions_label.setProperty("class", "Instructions")
        self.instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.combos = QWidget()
        combos_layout = QVBoxLayout(self.combos)
        self.combos.setProperty("class", "combos")

        grid = QGridLayout()
        combos_layout.addLayout(grid)

        self.manufacturerCombo = ComboWidget("Manufacturer", self)
        self.modelCombo = ComboWidget("Model", self)
        self.engineSizeCombo = ComboWidget("Engine Size", self)
        self.markSeriesCombo = ComboWidget("Mark Series", self)
        self.driveTypeCombo = ComboWidget("Drive Type", self)
        self.positionCombo = ComboWidget("Position", self)

        grid.addWidget(self.manufacturerCombo, 0, 0)
        grid.addWidget(self.modelCombo, 0, 1)
        grid.addWidget(self.engineSizeCombo, 1, 0)
        grid.addWidget(self.markSeriesCombo, 1, 1)
        grid.addWidget(self.driveTypeCombo, 2, 0)
        grid.addWidget(self.positionCombo, 2, 1)

        hlayout = QHBoxLayout()
        self.searchButton = QPushButton("Search")
        self.resetButton = QPushButton("Reset")
        combos_layout.addLayout(hlayout)
        hlayout.addWidget(self.searchButton)
        hlayout.addWidget(self.resetButton)

        layout.addWidget(self.logolabel)
        layout.addWidget(self.instructions_label)
        layout.addWidget(self.combos)

        self.bottom_image_label = QLabel()
        self.bottom_image_label.setPixmap(
            QPixmap(":main.JPG").scaledToHeight(
                300, Qt.TransformationMode.SmoothTransformation
            )
        )
        self.bottom_image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.bottom_image_label)
        layout.addWidget(self.footer)

        self.setup_ui_logic()
        self.populate_manufacturers()

    def populate_manufacturers(self):
        """Populates the manufacturer combo box with data from the database."""
        manufacturers = database.get_unique_manufacturers(DB_PATH)
        self.manufacturerCombo.addItems(manufacturers)

    def setup_ui_logic(self):
        """Connects signals to the appropriate slots for updating the UI based on user interactions."""
        self.manufacturerCombo.currentTextChanged.connect(self.update_models)
        self.modelCombo.currentTextChanged.connect(self.update_engine_sizes)
        self.engineSizeCombo.currentTextChanged.connect(self.update_mark_series)
        self.markSeriesCombo.currentTextChanged.connect(self.update_drive_types)
        self.driveTypeCombo.currentTextChanged.connect(self.update_positions)
        self.searchButton.clicked.connect(self.search_parts)
        self.resetButton.clicked.connect(self.reset_dropdowns)

    def update_models(self):
        """Updates the model dropdown based on the selected manufacturer."""
        self.clear_combo_box(self.modelCombo, "")
        selected_manufacturer = self.manufacturerCombo.currentText()
        if selected_manufacturer == "":
            self.clear_all_combo_boxes(except_boxes=["manufacturer"])
            return
        models = database.get_models(DB_PATH, selected_manufacturer)
        self.modelCombo.addItems(models)
        self.update_engine_sizes()

    def update_engine_sizes(self):
        """Updates the engine size combo box based on the selected model."""
        self.clear_combo_box(self.engineSizeCombo, "")
        selected_manufacturer = self.manufacturerCombo.currentText()
        selected_model = self.modelCombo.currentText()
        if selected_model == "":
            self.clear_all_combo_boxes(except_boxes=["manufacturer", "model"])
            return
        engine_sizes = database.get_engine_sizes(
            DB_PATH, selected_manufacturer, selected_model
        )
        self.engineSizeCombo.addItems(engine_sizes)
        self.update_mark_series()

    def update_mark_series(self):
        """Updates the mark series combo box based on the selected engine size."""
        self.clear_combo_box(self.markSeriesCombo, "")
        selected_manufacturer = self.manufacturerCombo.currentText()
        selected_model = self.modelCombo.currentText()
        selected_engine_size = self.engineSizeCombo.currentText()
        if selected_engine_size == "":
            self.clear_all_combo_boxes(
                except_boxes=["manufacturer", "model", "engine_size"]
            )
            return
        mark_series = database.get_mark_series(
            DB_PATH, selected_manufacturer, selected_model, selected_engine_size
        )
        self.markSeriesCombo.addItems(mark_series)
        self.update_drive_types()

    def update_drive_types(self):
        """Updates the drive type combo box based on the selected mark series."""
        self.clear_combo_box(self.driveTypeCombo, "")
        selected_manufacturer = self.manufacturerCombo.currentText()
        selected_model = self.modelCombo.currentText()
        selected_engine_size = self.engineSizeCombo.currentText()
        selected_mark_series = self.markSeriesCombo.currentText()
        if selected_mark_series == "":
            self.clear_all_combo_boxes(
                except_boxes=["manufacturer", "model", "engine_size", "mark_series"]
            )
            return
        drive_types = database.get_drive_types(
            DB_PATH,
            selected_manufacturer,
            selected_model,
            selected_engine_size,
            selected_mark_series,
        )
        self.driveTypeCombo.addItems(drive_types)
        self.update_positions()

    def update_positions(self):
        """Updates the position combo box based on the selected drive type."""
        self.clear_combo_box(self.positionCombo, "")
        selected_manufacturer = self.manufacturerCombo.currentText()
        selected_model = self.modelCombo.currentText()
        selected_engine_size = self.engineSizeCombo.currentText()
        selected_mark_series = self.markSeriesCombo.currentText()
        selected_drive_type = self.driveTypeCombo.currentText()
        if selected_drive_type == "":
            self.clear_all_combo_boxes(
                except_boxes=[
                    "manufacturer",
                    "model",
                    "engine_size",
                    "mark_series",
                    "drive_type",
                ]
            )
            return
        positions = database.get_positions(
            DB_PATH,
            selected_manufacturer,
            selected_model,
            selected_engine_size,
            selected_mark_series,
            selected_drive_type,
        )
        self.positionCombo.addItems(positions)

    def clear_combo_box(self, combo_box, placeholder):
        """Clears the given combo box and sets a placeholder item."""
        combo_box.clear()
        combo_box.addItem(placeholder)

    def clear_all_combo_boxes(self, except_boxes=None):
        """Clears all combo boxes except those specified."""
        if except_boxes is None:
            except_boxes = []
        if "model" not in except_boxes:
            self.clear_combo_box(self.modelCombo, "")
        if "engine_size" not in except_boxes:
            self.clear_combo_box(self.engineSizeCombo, "")
        if "mark_series" not in except_boxes:
            self.clear_combo_box(self.markSeriesCombo, "")
        if "drive_type" not in except_boxes:
            self.clear_combo_box(self.driveTypeCombo, "")
        if "position" not in except_boxes:
            self.clear_combo_box(self.positionCombo, "")

    def reset_dropdowns(self):
        """Resets all dropdowns to their initial state and repopulates manufacturers."""
        self.clear_all_combo_boxes()
        self.clear_combo_box(self.manufacturerCombo, "")
        self.populate_manufacturers()
        self.clearResults.emit()

    def search_parts(self):
        """Searches for parts based on selected criteria and displays the results."""
        manufacturer = self.manufacturerCombo.currentText()
        model = self.modelCombo.currentText()
        engine_size = self.engineSizeCombo.currentText()
        mark_series = self.markSeriesCombo.currentText()
        drive_type = self.driveTypeCombo.currentText()
        position = self.positionCombo.currentText()

        criteria = {
            "manufacturer": (manufacturer if manufacturer else None),
            "model": model if model else None,
            "engine_size": engine_size if engine_size else None,
            "mark_series": mark_series if mark_series else None,
            "drive_type": drive_type if drive_type else None,
            "position": position if position else None,
        }
        parts = database.get_parts(DB_PATH, criteria)
        self.displayResults.emit(parts)


class PartWidget(QWidget):
    def __init__(self, part_number, part_size, tech_note_1, tech_note_2, parent=None):
        super().__init__(parent=parent)
        self.setProperty("class", "PartWidget")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self._parent = parent
        part_layout = QHBoxLayout(self)

        label_layout = QVBoxLayout()
        label_layout.setAlignment(Qt.AlignCenter)

        part_number_label = QLabel(f"<b>{part_number}</b>")
        part_number_label.setAlignment(Qt.AlignCenter)
        part_number_label.setStyleSheet("font-size: 20px; padding: 5px;")
        label_layout.addWidget(part_number_label)

        part_size_label = QLabel(part_size)
        part_size_label.setAlignment(Qt.AlignCenter)
        part_size_label.setStyleSheet("padding: 5px;")
        part_size_label.setWordWrap(True)
        label_layout.addWidget(part_size_label)

        tech_note_1_label = QLabel(
            f"Tech Note 1: {tech_note_1 if tech_note_1 else 'N/A'}"
        )
        tech_note_1_label.setAlignment(Qt.AlignCenter)
        tech_note_1_label.setStyleSheet("font-size: 14px; padding: 5px;")
        tech_note_1_label.setWordWrap(True)
        label_layout.addWidget(tech_note_1_label)

        tech_note_2_label = QLabel(
            f"Tech Note 2: {tech_note_2 if tech_note_2 else 'N/A'}"
        )
        tech_note_2_label.setAlignment(Qt.AlignCenter)
        tech_note_2_label.setStyleSheet("font-size: 14px; padding: 5px;")
        tech_note_2_label.setWordWrap(True)
        label_layout.addWidget(tech_note_2_label)

        label_layout.addStretch(1)
        part_layout.addLayout(label_layout)

        self.image_label = QLabel()
        if part_number:
            self.image_path = str(
                ASSETS / "wheelbearing_images_LSODS" / f"{part_number}.png"
            )
        else:
            self.image_path = ":title.jpg"
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(
            pixmap.scaledToHeight(200, Qt.TransformationMode.SmoothTransformation)
        )
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.mousePressEvent = (
            lambda event, path=self.image_path: self._parent.show_image_modal(path)
        )
        part_layout.addWidget(self.image_label)

        self.setMinimumHeight(300)
        self.setFixedSize(self._parent.scroll.viewport().width() - 20, 300)

    def resize_part(self):
        w = self._parent.scroll.viewport().width()
        self.setFixedSize(w - 20, 300)
        pixmap = QPixmap(self.image_path).scaledToHeight(
            200, Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(pixmap)

    def resize_part(self):
        w = self._parent.scroll.viewport().width()
        self.setFixedSize(w - 20, 250)
        pixmap = QPixmap(self.image_path).scaledToHeight(
            200, Qt.TransformationMode.SmoothTransformation
        )
        if pixmap.isNull():
            print(f"[ERROR] Failed to reload image at path: {self.image_path}")
        else:
            print(f"[DEBUG] Resizing and setting image: {self.image_path}")
        self.image_label.setPixmap(pixmap)


class RightSide(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setProperty("class", "RightSide")

        layout = QVBoxLayout(self)

        self.scroll = QScrollArea()
        self.scroll.setWidget(QWidget())
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumWidth(300)
        self.scroll.widget().setFixedWidth(self.scroll.viewport().width())
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(self.scroll)

        self.part_widgets = []

    def clear_results(self):
        """Clears the results area in the UI."""
        self.scroll.widget().deleteLater()
        widget = QWidget()
        widget.setFixedWidth(self.scroll.viewport().width())

        self.layout = QVBoxLayout(widget)
        self.scroll.setWidget(widget)
        self.scroll.setWidgetResizable(True)

    def show_image_modal(self, image_path):
        """Shows a modal dialog with a larger view of the clicked image."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Image Preview")
        dialog.setModal(True)
        layout = QVBoxLayout()

        pixmap = QPixmap(image_path)
        label = QLabel()
        label.setPixmap(pixmap)
        layout.addWidget(label)

        dialog.setLayout(layout)
        dialog.exec_()

    def display_results(self, parts):
        """Displays the search results in the results area."""
        self.clear_results()
        self.part_widgets = []
        for part in parts:
            part_number, part_size, tech_note_1, tech_note_2 = part
            part_widget = PartWidget(
                part_number, part_size, tech_note_1, tech_note_2, parent=self
            )
            self.layout.addWidget(part_widget, alignment=Qt.AlignTop | Qt.AlignLeft)
            self.part_widgets.append(part_widget)

    def resizeEvent(self, event):
        for part in self.part_widgets:
            part.resize_part()
        super().resizeEvent(event)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.hlayout = QHBoxLayout(self.central)

        self.left_side = LeftSide()
        self.right_side = RightSide()

        self.left_side.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.right_side.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.Preferred
        )

        self.hlayout.addWidget(self.left_side, 2)
        self.hlayout.addWidget(self.right_side, 1)

        self.hlayout.setSpacing(0)
        self.hlayout.setContentsMargins(0, 0, 0, 0)

        self.left_side.displayResults.connect(self.right_side.display_results)
        self.left_side.clearResults.connect(self.right_side.clear_results)

    def resizeEvent(self, event):

        self.left_side.logolabel.setFixedHeight(self.left_side.height() * 0.1)
        self.left_side.logolabel.setPixmap(
            QPixmap(":new-logo.PNG").scaled(
                self.left_side.width(),
                self.left_side.height() * 0.1,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.right_side.scroll.widget().setFixedWidth(
            self.right_side.scroll.viewport().width()
        )
        super().resizeEvent(event)
