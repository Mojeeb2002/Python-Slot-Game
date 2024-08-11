# Modern Slot Machine Game

Welcome to the Modern Slot Machine Game! This is a Python-based graphical slot machine simulator built with PyQt5. It offers a sleek, modern interface and realistic slot machine mechanics for an engaging gaming experience.

## 🎰 Features

- Modern, attractive GUI built with PyQt5
- Customizable bet amounts and number of lines
- Realistic slot machine mechanics
- Animated spin feature
- In-game deposit system
- Responsive design with custom-styled buttons

## 🛠 Installation

### Prerequisites

- Python 3.6 or higher
- PyQt5

### Steps

1. Clone this repository:
   ```
   git clone https://github.com/Mojeeb2002/Python-Slot-Game.git
   ```

2. Install the required dependencies:
   ```
   pip install PyQt5
   ```

3. Run the game:
   ```
   python main_gui.py
   ```

## 🎮 How to Play

1. **Deposit Money**: Start by depositing money into your balance using the deposit input field and button.

2. **Place Your Bet**: Enter your bet amount and the number of lines you want to bet on (1-3).

3. **Spin**: Click the "Spin" button to play. The slot machine will animate and display the results.

4. **Win or Lose**: Your winnings (if any) will be displayed, and your balance will be updated accordingly.

5. **Keep Playing**: Continue playing as long as you have sufficient balance. You can deposit more money at any time.

## 🖥 Game Interface

- **Balance Display**: Shows your current balance at the top of the window.
- **Deposit Section**: Allows you to add more money to your balance.
- **Betting Section**: Input fields for your bet amount and number of lines.
- **Spin Button**: Starts the game with your current bet.
- **Slot Display**: Shows the result of each spin with fruit emojis.
- **Result Label**: Displays the outcome of each spin, including winnings and winning lines.

## 🛠 Customization

You can easily customize various aspects of the game:

- Modify the `symbol_count` and `symbol_value` dictionaries to change the symbols and their frequencies/values.
- Adjust the `MIN_BET` and `MAX_LINES` constants to alter betting limits.
- Modify the color scheme by updating the stylesheet in the `SlotMachineGUI` class.

## 🤝 Contributing

Contributions to improve the game are welcome! Please feel free to submit a Pull Request.


## 🙏 Acknowledgements

- PyQt5 for providing the GUI framework
- Emoji graphics provided by the Unicode Consortium

Enjoy the game, and may luck be on your side! 🍀
