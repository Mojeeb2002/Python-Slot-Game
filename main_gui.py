import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QMessageBox, QFrame, QDialog)
from PyQt5.QtGui import QFont, QColor, QPainter
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect

MAX_LINES = 3
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "🍒": 2,
    "🍊": 4,
    "🍋": 6,
    "🍇": 8
}

symbol_value = {
    "🍒": 5,
    "🍊": 4,
    "🍋": 3,
    "🍇": 2
}

class RoundedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(200, 50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.isDown():
            color = QColor("#2980B9")
        elif self.underMouse():
            color = QColor("#3498DB")
        else:
            color = QColor("#2C3E50")

        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 25, 25)

        painter.setPen(Qt.white)
        painter.setFont(QFont('Arial', 12, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

class DepositDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Deposit More")
        self.setFixedSize(300, 150)
        layout = QVBoxLayout()

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter deposit amount")
        layout.addWidget(self.amount_input)

        deposit_button = RoundedButton("Deposit")
        deposit_button.clicked.connect(self.accept)
        layout.addWidget(deposit_button)

        self.setLayout(layout)

    def get_amount(self):
        return int(self.amount_input.text()) if self.amount_input.text().isdigit() else 0

class SlotMachineGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎰 Modern Slot Machine")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1A1A2E;
            }
            QLabel {
                color: #E94560;
            }
            QLineEdit {
                background-color: #16213E;
                color: #E94560;
                border: 2px solid #0F3460;
                border-radius: 10px;
                padding: 5px;
            }
        """)

        self.balance = 0
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Title
        title_label = QLabel("🎰 Modern Slot Machine")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title_label)

        # Balance display
        self.balance_label = QLabel(f"Balance: ${self.balance}")
        self.balance_label.setAlignment(Qt.AlignCenter)
        self.balance_label.setFont(QFont('Arial', 18))
        layout.addWidget(self.balance_label)

        # Deposit input
        deposit_layout = QHBoxLayout()
        self.deposit_input = QLineEdit()
        self.deposit_input.setPlaceholderText("Enter amount")
        deposit_button = RoundedButton("Deposit")
        deposit_button.clicked.connect(self.deposit)
        deposit_layout.addWidget(self.deposit_input)
        deposit_layout.addWidget(deposit_button)
        layout.addLayout(deposit_layout)

        # Bet input
        bet_layout = QHBoxLayout()
        self.bet_input = QLineEdit()
        self.bet_input.setPlaceholderText(f"Bet amount (min: ${MIN_BET})")
        self.lines_input = QLineEdit()
        self.lines_input.setPlaceholderText(f"Lines (1-{MAX_LINES})")
        bet_layout.addWidget(self.bet_input)
        bet_layout.addWidget(self.lines_input)
        layout.addLayout(bet_layout)

        # Spin button
        spin_button = RoundedButton("🎲 Spin")
        spin_button.clicked.connect(self.spin)
        layout.addWidget(spin_button, alignment=Qt.AlignCenter)

        # Slot machine display
        self.slot_display = QLabel("🎰 🎰 🎰\n🎰 🎰 🎰\n🎰 🎰 🎰")
        self.slot_display.setAlignment(Qt.AlignCenter)
        self.slot_display.setFont(QFont('Arial', 24))
        self.slot_display.setStyleSheet("""
            QLabel {
                background-color: #0F3460;
                border: 2px solid #E94560;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        layout.addWidget(self.slot_display)

        # Result display
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont('Arial', 14))
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

        central_widget.setLayout(layout)

    def deposit(self):
        amount = self.deposit_input.text()
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                self.balance += amount
                self.update_balance()
                self.deposit_input.clear()
            else:
                self.show_message("Error", "Amount must be greater than zero.")
        else:
            self.show_message("Error", "Please enter a valid amount.")

    def update_balance(self):
        self.balance_label.setText(f"Balance: ${self.balance}")

    def spin(self):
        bet = self.bet_input.text()
        lines = self.lines_input.text()

        if not bet.isdigit() or not lines.isdigit():
            self.show_message("Error", "Please enter valid numbers for bet and lines.")
            return

        bet = int(bet)
        lines = int(lines)

        if bet < MIN_BET:
            self.show_message("Error", f"Minimum bet is ${MIN_BET}.")
            return

        if not (1 <= lines <= MAX_LINES):
            self.show_message("Error", f"You can only bet on 1 to {MAX_LINES} lines.")
            return

        total_bet = bet * lines
        if total_bet > self.balance:
            reply = QMessageBox.question(self, 'Insufficient Funds',
                                         "You don't have enough balance. Would you like to deposit more?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.prompt_deposit()
            return

        # Perform the spin
        slots = self.get_slot_machine_spin(ROWS, COLS, symbol_count)
        self.animate_spin(slots)
        winnings, winning_lines = self.check_winnings(slots, lines, bet, symbol_value)

        # Update balance and display results
        self.balance += winnings - total_bet
        self.update_balance()

        result_text = f"You bet ${total_bet} and won ${winnings}!\n"
        if winning_lines:
            result_text += f"Winning lines: {', '.join(map(str, winning_lines))}"
        else:
            result_text += "No winning lines."
        self.result_label.setText(result_text)

    def prompt_deposit(self):
        dialog = DepositDialog(self)
        if dialog.exec_():
            amount = dialog.get_amount()
            if amount > 0:
                self.balance += amount
                self.update_balance()
            else:
                self.show_message("Error", "Invalid deposit amount.")

    def get_slot_machine_spin(self, rows, cols, symbols):
        all_symbols = []
        for symbol, symbol_count in symbols.items():
            all_symbols.extend([symbol] * symbol_count)

        columns = []
        for _ in range(cols):
            column = random.sample(all_symbols, rows)
            columns.append(column)

        return columns

    def animate_spin(self, final_slots):
        frames = 20
        for _ in range(frames):
            random_slots = self.get_slot_machine_spin(ROWS, COLS, symbol_count)
            self.display_slots(random_slots)
            QApplication.processEvents()
        self.display_slots(final_slots)

    def display_slots(self, columns):
        display_text = ""
        for row in range(ROWS):
            for col in range(COLS):
                display_text += f"{columns[col][row]} "
            display_text = display_text.strip() + "\n"
        self.slot_display.setText(display_text.strip())

    def check_winnings(self, columns, lines, bet, values):
        winnings = 0
        winning_lines = []
        for line in range(min(lines, ROWS)):
            symbol = columns[0][line]
            for column in columns:
                symbol_to_check = column[line]
                if symbol != symbol_to_check:
                    break
            else:
                winnings += values[symbol] * bet
                winning_lines.append(line + 1)

        return winnings, winning_lines

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    slot_machine = SlotMachineGUI()
    slot_machine.show()
    sys.exit(app.exec_())