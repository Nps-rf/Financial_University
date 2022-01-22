from typing import NewType, Callable
Menu = NewType('Menu', str)  # Path to menu file
Button = NewType('Button', int)  # Number of button
Buttons = NewType('Button', [Button])  # All Buttons
Action_Info = NewType('Action_Info', str)  # Information about performed turn
Available_moves = NewType('Available_moves', list)  # List of available squares
