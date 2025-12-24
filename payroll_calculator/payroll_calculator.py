from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QSizePolicy, QPushButton
from PyQt5.QtGui import QIcon, QFont, QFontMetrics
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()  

        self.calculate_button.clicked.connect(self.calculate_earnings)
        self.regular_time_hours_input.textChanged.connect(self.get_regular_time_total_hours)
        self.regular_time_minutes_input.textChanged.connect(self.get_regular_time_total_minutes)
        self.overtime_time_hours_input.textChanged.connect(self.get_overtime_time_total_hours)
        self.overtime_time_minutes_input.textChanged.connect(self.get_overtime_time_total_minutes)

        self.regular_time_total_hours = 0
        self.regular_time_total_minutes = 0
        self.overtime_time_total_hours = 0
        self.overtime_time_total_minutes = 0
        self.total_time = 0

        self.centralWidget().setFocus() # Disables focus on any widget, user will have to click on an input field to start typing
    
    def set_window(self):
        self.setWindowTitle("Payroll Calculator")
        self.setWindowIcon(QIcon("payroll_calculator/payroll_calculator.ico"))
        self.setMinimumSize(750, 800)
        self.setStyleSheet("background-color: #f7e2c7")

    def initUI(self):
        self.set_window()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout()
        central_widget.setLayout(main_layout)

        self.create_labels()
        self.create_input_fields()
        self.create_buttons()

        self.all_widgets = {**self.labels, **self.input_fields, **self.buttons}
        
        self.add_widgets(layout=main_layout)
        self.set_placeholder_text()
    
    def create_labels(self):
        # Labels
        regular_time_label = QLabel("Regular Time")
        overtime_time_label = QLabel("Overtime Time")
        salary_label = QLabel("Salary")
        hourly_wage_label = QLabel("Hourly Wage")
        bonuses_label = QLabel("Bonuses")
        tax_rate_label = QLabel("Tax Rate")
        self.gross_pay_label = QLabel("Gross Pay- ")
        self.deductions_label = QLabel("Deductions- ")
        self.net_pay_label = QLabel("Net Pay- ")
        self.total_time_label = QLabel("Total Hours- ")

        self.labels = {
            # ((row, col, rowspan, colspan), (row, row stretch), font size): label
            ((0, 0, 1, 2), (0, 2), 25): regular_time_label,
            ((0, 2, 1, 2), (0, 2), 25): overtime_time_label,
            ((2, 0, 1, 4), (2, 1), 12): self.total_time_label,
            ((3, 0, 1, 2), (3, 2), 25): salary_label,
            ((3, 2, 1, 2), (3, 2), 25): hourly_wage_label,
            ((5, 0, 1, 2), (5, 2), 25): bonuses_label,
            ((5, 2, 1, 2), (5, 2), 25): tax_rate_label,
            ((8, 0, 1, 4), (8, 1), 12): self.gross_pay_label,
            ((9, 0, 1, 4), (9, 1), 12): self.deductions_label,
            ((10, 0, 1, 4), (10, 1), 12): self.net_pay_label
        }

        for layout_coords_and_row_stretch_and_font, label in self.labels.items():
            if label == self.total_time_label or label == self.gross_pay_label or label == self.deductions_label or label == self.net_pay_label:
                label.setStyleSheet("background-color: #578e87")
            else:
                label.setStyleSheet("background-color: #4C991F; border: 1px solid black")

            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            label.setAlignment(Qt.AlignCenter)
    
    def create_input_fields(self):
        # Input Fields
        self.regular_time_hours_input = HighlightAllTextQLineEdit("Enter hours worked")
        self.regular_time_minutes_input = HighlightAllTextQLineEdit("Enter minutes worked")
        self.overtime_time_hours_input = HighlightAllTextQLineEdit("Enter hours worked")
        self.overtime_time_minutes_input = HighlightAllTextQLineEdit("Enter minutes worked")
        self.salary_input = HighlightAllTextQLineEdit("Enter salary")
        self.hourly_wage_input = HighlightAllTextQLineEdit("Enter hourly wage")
        self.bonuses_input = HighlightAllTextQLineEdit("Enter bonuses")
        self.tax_rate_input = HighlightAllTextQLineEdit("Enter tax rate (0.xx)")

        # ((row, col, rowspan, colspan), (row, row stretch), font size): input field
        self.input_fields = {
            ((1, 0), (1, 2), 12): self.regular_time_hours_input,
            ((1, 1), (1, 2), 12): self.regular_time_minutes_input,
            ((1, 2), (1, 2), 12): self.overtime_time_hours_input,
            ((1, 3), (1, 2), 12): self.overtime_time_minutes_input,
            ((4, 0, 1, 2), (4, 2), 12): self.salary_input,
            ((4, 2, 1, 2), (4, 2), 12): self.hourly_wage_input,
            ((6, 0, 1, 2), (6, 2), 12): self.bonuses_input,
            ((6, 2, 1, 2), (6, 2), 12): self.tax_rate_input
        }

        for layout_coords_and_row_stretch_and_font, input_field in self.input_fields.items():
            input_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            input_field.setStyleSheet(f"""
                                    QLineEdit {{
                                        background-color: #D0E8C0; 
                                        border: 2px solid #8F9779;
                                    }}

                                    QLineEdit:hover {{
                                        border: 2px solid black;
                                        border-radius: 10px
                                    }}
                                    """)
    
    def create_buttons(self):
        # Buttons
        self.calculate_button = QPushButton("Calculate Earnings")

        # ((row, col, rowspan, colspan), (row, row stretch), font size): button
        self.buttons = {
            ((7, 0, 1, 4), (7, 2), 15): self.calculate_button
        }

        self.calculate_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.calculate_button.setStyleSheet(f"""
                                    QPushButton {{
                                        background-color: #3D7316;
                                    }}

                                    QPushButton:hover {{
                                        background-color: #8A9A5B;
                                    }}
                                       
                                    QPushButton:pressed {{
                                       background-color: #9CAF88;
                                    }}
                                    """)
        
    def add_widgets(self, layout):
        for layout_coords_and_row_stretch_and_font, widget in self.all_widgets.items():
            layout.addWidget(widget, *layout_coords_and_row_stretch_and_font[0])
            layout.setRowStretch(*layout_coords_and_row_stretch_and_font[1])

    def set_placeholder_text(self):
        for layout_coords_and_row_stretch_and_font, input_field in self.input_fields.items():
            input_field.setPlaceholderText(input_field.text())
    
    def calculate_earnings(self):
        try:
            salary = float(self.salary_input.text())
            hourly_wage = float(self.hourly_wage_input.text())
            hourly_wage_money_made = (hourly_wage * self.regular_time) + (hourly_wage * self.overtime_time * 1.5)
            bonuses = float(self.bonuses_input.text())
            tax_rate = float(self.tax_rate_input.text())
            
            earnings = round(salary + hourly_wage_money_made + bonuses, 2)
            deductions = round(earnings * tax_rate, 2)
            net_pay = round(earnings - deductions, 2)

            self.set_earnings_text(earnings=earnings, deductions=deductions, net_pay=net_pay)
        except ValueError:
            pass

    def calculate_total_time(self):
        try:
            self.regular_time = float(self.regular_time_total_hours) + float(self.regular_time_total_minutes) / 60
            self.overtime_time = float(self.overtime_time_total_hours) + float(self.overtime_time_total_minutes) / 60
            self.total_time = round(self.regular_time + self.overtime_time, 2)

            self.set_total_time_text()
        except ValueError:
            pass
    
    def set_earnings_text(self, earnings, deductions, net_pay):
        self.gross_pay_label.setText(f"Gross Pay- ${earnings:,}")
        self.deductions_label.setText(f"Deductions- ${deductions:,}")
        self.net_pay_label.setText(f"Net Pay- ${net_pay:,}")

    def set_total_time_text(self):
        self.total_time_label.setText(f"Total Hours- {self.total_time}")

    def get_regular_time_total_hours(self):
        self.regular_time_total_hours = self.sender().text()
        if self.regular_time_total_hours == "":
            self.regular_time_total_hours = 0
        self.calculate_total_time() 

    def get_regular_time_total_minutes(self):
        self.regular_time_total_minutes = self.sender().text()
        if self.regular_time_total_minutes == "":
            self.regular_time_total_minutes = 0
        self.calculate_total_time()

    def get_overtime_time_total_hours(self):
        self.overtime_time_total_hours = self.sender().text()
        if self.overtime_time_total_hours == "":
            self.overtime_time_total_hours = 0
        self.calculate_total_time()

    def get_overtime_time_total_minutes(self):
        self.overtime_time_total_minutes = self.sender().text()
        if self.overtime_time_total_minutes == "":
            self.overtime_time_total_minutes = 0
        self.calculate_total_time()

    def resize_font(self):
        for layout_coords_and_row_stretch_and_font, widget in self.all_widgets.items():
            font = widget.font()
            metrics = QFontMetrics(font)
            text_size = metrics.horizontalAdvance(widget.text())
            input_field_width = widget.width()
            font_size = layout_coords_and_row_stretch_and_font[2]

            while text_size >= input_field_width - 25:
                font_size -= 1
                widget.setFont(QFont("Lato", font_size, QFont.DemiBold))
                font = widget.font()
                metrics = QFontMetrics(font)
                text_size = metrics.horizontalAdvance(widget.text())
            else:
                font_size += 1
                widget.setFont(QFont("Lato", font_size, QFont.DemiBold))

    def resizeEvent(self, a0):
        self.resize_font()

# Highlights all text in the input field
# Has all of the same properties as a regular QLineEdit
class HighlightAllTextQLineEdit(QLineEdit):
    def mousePressEvent(self, a0):
        self.selectAll()

app = QApplication([])
window = MainWindow()
window.show()
window.resize_font()
app.exec()
