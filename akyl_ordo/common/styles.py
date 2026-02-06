PRIMARY = "#3F51B5"
SECONDARY = "#2196F3"
SUCCESS = "#4CAF50"
ERROR = "#F44336"
BACKGROUND = "#F5F7FB"
CARD = "#FFFFFF"

APP_STYLE = f"""
QWidget {{
  background-color: {BACKGROUND};
  color: #1f1f1f;
  font-size: 14px;
}}
QPushButton {{
  background-color: {PRIMARY};
  color: white;
  border: none;
  border-radius: 16px;
  padding: 10px 16px;
  font-weight: 600;
}}
QPushButton:disabled {{
  background-color: #b0b4d0;
}}
QLineEdit, QTextEdit, QComboBox, QSpinBox {{
  background-color: {CARD};
  border-radius: 12px;
  padding: 8px 10px;
  border: 1px solid #d7dbe8;
}}
QGroupBox {{
  border: 1px solid #d7dbe8;
  border-radius: 16px;
  margin-top: 10px;
}}
QGroupBox::title {{
  subcontrol-origin: margin;
  left: 16px;
  padding: 0 4px;
}}
"""
