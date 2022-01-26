from typing import NewType, Callable
Menu = NewType('TypeMenu', str)  # Path to menu file
Button = NewType('TypeButton', int)  # Number of button
Buttons = NewType('TypeButtons', [Button])  # All Buttons
Action_Info = NewType('TypeAction_Info', str)  # Information about performed turn
Available_moves = NewType('TypeAvailable_moves', list)  # List of available squares
