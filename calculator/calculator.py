from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGridLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QFontMetrics
from math import sqrt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.keys = {}
        self.create_keys(min=7, max=10, row=3)
        self.create_keys(min=4, max=7, row=4)
        self.create_keys(min=1, max=4, row=5)
        self.create_keys(min=0, max=1, row=6)
        
        self.initUI()

        self.setWindowTitle("Calculator")
        self.setMinimumSize(QSize(450, 750))
        self.setWindowIcon(QIcon("calculator\calculator_icon.ico"))
        self.setStyleSheet("background-color: #1E1B2C")

        for key, button in self.key_widgets.items():
            if key != "key_display":
                button.clicked.connect(self.set_display_text)

        self.current_entry = ""
    
    def create_keys(self, min: int, max: int, row: int) -> None:
        # Sets position of key0
        if min == 0 and max == 1:
            self.keys[f"key0"] = {"key": f"0", "row": 6, "column": 1, "background-color": "#2A2438"}
            return
        
        # Sets positions of keys 1-9
        for col, x in enumerate(range(min, max)):
            if col >= 4:
                col = 0
            self.keys[f"key{x}"] = {"key": f"{x}", "row": row, "column": col, "background-color": "#2A2438"}

        self.special_keys = {
            "key_display": {"key": "", "row": 0, "column": 0, "row_span": 1, "column_span": 4, "background-color": "#1B1530"},

            # Column 0
            "key_percent": {"key": "%", "row": 1, "column": 0, "background-color": "#4B3E66"},
            "key_fraction": {"key": "1/x", "row": 2, "column": 0, "background-color": "#4B3E66"},
            "key_plus_minus": {"key": "±", "row": 6, "column": 0, "background-color": "#4B3E66"},
          
            # Column 1
            "key_clear_entry": {"key": "CE", "row": 1, "column": 1, "background-color": "#4B3E66"}, 
            "key_square": {"key": "x²", "row": 2, "column": 1, "background-color": "#6C4BA1"},

            # Column 2
            "key_clear": {"key": "C", "row": 1, "column": 2, "background-color": "#4B3E66"},
            "key_square_root": {"key": "²√x", "row": 2, "column": 2, "background-color": "#6C4BA1"},
            "key_decimal": {"key": ".", "row": 6, "column": 2, "background-color": "#2A2438"},

            # Column 3
            "key_delete": {"key": "⌫", "row": 1, "column": 3, "background-color": "#4B3E66"},
            "key_divide": {"key": "÷", "row": 2, "column": 3, "background-color": "#9B59B6"}, 
            "key_multiply": {"key": "×", "row": 3, "column": 3, "background-color": "#9B59B6"},  
            "key_minus": {"key": "-", "row": 4, "column": 3, "background-color": "#9B59B6"},
            "key_plus": {"key": "+", "row": 5, "column": 3, "background-color": "#9B59B6"},
            "key_equals": {"key": "=", "row": 6, "column": 3, "background-color": "#8E44AD"},  
        }

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        grid = QGridLayout()
        central_widget.setLayout(grid)

        self.all_keys = {**self.keys, **self.special_keys}  # Stores a combined dictionary of self.keys and self.special_keys
        self.key_widgets = {}   # Stores memory locations of QPushButtons()

        for key, value in self.all_keys.items():
            key_symbol = value["key"]
            key_position = value["row"], value["column"]
            
            # Sets properties of the calculator display
            if key == "key_display":
                self.key_widgets[key] = QLabel()
                self.key_widgets[key].setFixedHeight(175)
                self.key_widgets[key].setAlignment(Qt.AlignRight | Qt.AlignCenter)  # Aligns text to the right, still in the center

                display_span = value["row_span"], value["column_span"]
                grid.addWidget(self.key_widgets[key], *key_position, *display_span)   # Spans 1 row, 4 columns
                
            # Sets properties of every other widget
            else:
                self.key_widgets[key] = QPushButton(key_symbol)
                grid.addWidget(self.key_widgets[key], *key_position)

            # Sets a different font size for the display and every other key
            # Also sets style sheet for the display
            for key, widget in self.key_widgets.items():
                if key != "key_display":
                    widget.setFont(QFont("Segoe UI", 36, QFont.Medium))
                else:
                    self.display_font_size = 50
                    widget.setFont(QFont("Segoe UI", self.display_font_size, QFont.Medium))
                    widget.setStyleSheet("color: #FFFFFF")
            
            # Sets style sheet for every key but the display
            self.key_widgets[key].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.key_widgets[key].setStyleSheet(f"""
                QPushButton {{
                    background-color: {value["background-color"]};  
                    color: #FFFFFF;           
                    border-radius: 10px;
                    font-size: 18px;
                }}
                QPushButton:hover {{
                    background-color: #3C2F50;  
                    color: #FFD700;           
                }}
                QPushButton:pressed {{
                    background-color: #9B59B6; 
                    color: #FFFFFF;             
                }}
            """)

    def set_display_text(self, keyboard_key=None, backspace=False):
        if backspace == True:
            self.current_entry = self.current_entry[0:len(self.current_entry) - 1]

        elif keyboard_key != None and keyboard_key != False:  # Qt signal sends self.set_display_text(False) when clicking a button, this prevents that
            self.current_entry = self.current_entry + str(keyboard_key)
        
        else:
            key_memory_address = app.sender()   # Detects if and which button was clicked, is a memory address. None if method is called instead of button being clicked.
            for key in self.key_widgets:
                if key_memory_address == self.key_widgets[key]:
                    if key in self.special_keys:
                        self.current_entry = self.do_special_key_function(special_key=key)
                    else:
                        self.current_entry = self.current_entry + self.all_keys[key]["key"]  # Gets the button's text

        # Will update text even if no button is clicked, meaning input is done through the keyboard, such as using shift+5 (percent)
        self.key_widgets["key_display"].setText(f"{self.current_entry}") 
        self.scale_font()

    def do_special_key_function(self, special_key: str) -> str:
        operators = {
            "÷": "/",
            "×": "*",
            "-": "-",
            "+": "+",
            "²": "**2"
        }

        match special_key:
            case "key_clear" | "key_clear_entry":
                result = ""
            case "key_decimal":
                result = self.current_entry + "."
            case "key_delete":
                result = self.current_entry[0:len(self.current_entry) - 1]
            case "key_divide":
                result = self.current_entry + "÷"
            case "key_equals":
                for operator, python_operator in operators.items():
                    if operator in self.current_entry:
                        self.current_entry = self.current_entry.replace(operator, python_operator)
                        
                result = str(round(eval(self.current_entry), 10))
                result = self.check_if_int_or_float(number=result)
            case "key_fraction":
                result = str(round(eval("1 /" + self.current_entry), 10))
                result = self.check_if_int_or_float(number=result)
            case "key_minus":
                result = self.current_entry + "-"
            case "key_multiply":
                result = self.current_entry + "×"
            case "key_percent":
                result = str(round(eval(self.current_entry + "/ 100"), 10))
                result = self.check_if_int_or_float(number=result)
            case "key_plus":
                result = self.current_entry + "+"
            case "key_plus_minus":
                if self.current_entry[0] == "-":
                    result = self.current_entry[1:]
                else:
                    result = "-" + self.current_entry
            case "key_square":
                result = str(round(eval(self.current_entry + "** 2"), 10))
                result = self.check_if_int_or_float(number=result)
            case "key_square_root":
                result = str(round(sqrt(eval(self.current_entry)), 10))
                result = self.check_if_int_or_float(number=result)

        return result
    
    def check_if_int_or_float(self, number):
        if "." in number:
            decimal_index = number.index(".")
            if number[decimal_index:] == ".0":
                number = str(int(float(number)))
        return number

    def clear_display(self):
        self.current_entry = ""
        self.key_widgets["key_display"].setText(self.current_entry)

    def keyPressEvent(self, a0):
        qt_keys = [
            Qt.Key_0, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4,
            Qt.Key_5, Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9,

            Qt.Key_Plus, Qt.Key_Minus, Qt.Key_Asterisk, Qt.Key_Slash,       
                                
            Qt.Key_Period, Qt.Key_Percent, Qt.Key_Backspace, Qt.Key_Return, Qt.Key_Enter,     
        ]

        if a0.key() in qt_keys:
            match a0.key():
                case Qt.Key_Backspace:
                    self.scale_font(backspace=True)
                    self.set_display_text(backspace=True)
                case Qt.Key_Percent:
                    self.current_entry = self.do_special_key_function(special_key="key_percent")
                    self.set_display_text()
                case Qt.Key_Asterisk:
                    self.current_entry = self.do_special_key_function(special_key="key_multiply")
                    self.set_display_text()
                case Qt.Key_Slash:
                    self.current_entry = self.do_special_key_function(special_key="key_divide")
                    self.set_display_text()
                case Qt.Key_Enter | Qt.Key_Return:  # Enter = enter on numpad, Return = enter on home row
                    self.current_entry = self.do_special_key_function(special_key="key_equals")
                    self.set_display_text()
                case _:
                    keyboard_key = a0.text()
                    self.set_display_text(keyboard_key=keyboard_key)
                
    def scale_font(self, backspace=False):
        font = self.key_widgets["key_display"].font()
        metrics = QFontMetrics(font)
        current_text_space_taken = metrics.horizontalAdvance(self.key_widgets["key_display"].text()) 
        total_text_space = self.key_widgets["key_display"].width()

        if self.display_font_size != 10 and backspace == False:
            while current_text_space_taken >= total_text_space:
                font = self.key_widgets["key_display"].font()
                metrics = QFontMetrics(font)
                
                # Prevents font size from going under minimum
                if self.display_font_size == 10:
                    break
                else:
                    self.display_font_size -= 1
                
                self.key_widgets["key_display"].setFont(QFont("Segoe UI", self.display_font_size, QFont.Medium))
                current_text_space_taken = metrics.horizontalAdvance(self.key_widgets["key_display"].text()) 

        elif self.display_font_size <= 49 and backspace == True:
            while current_text_space_taken < total_text_space:
                font = self.key_widgets["key_display"].font()
                metrics = QFontMetrics(font)

                # Prevents font size from going above maximum
                if self.display_font_size == 50:
                    break
                else:
                    self.display_font_size += 1

                self.key_widgets["key_display"].setFont(QFont("Segoe UI", self.display_font_size, QFont.Medium))
                current_text_space_taken = metrics.horizontalAdvance(self.key_widgets["key_display"].text())

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
