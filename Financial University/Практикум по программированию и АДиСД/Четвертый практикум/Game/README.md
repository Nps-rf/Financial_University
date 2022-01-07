<img src="https://cdn1.iconfinder.com/data/icons/filled-line-christmas-icons/75/_deer-256.png" align="right"/>


# ♛ Chess game ♛
____
![https://img.shields.io/badge/Python-3.8-blue](https://img.shields.io/badge/Python-3.8-blue)
![https://img.shields.io/badge/Status-WIP-red](https://img.shields.io/badge/Status-WIP-red)

## About
* **This is an implementation of fourth workshop**
* **Based on [pygame](https://www.pygame.org/)**
* **Most requirements are done ✅**

## Structure
### Abbreviations scheme:
#### Full name
* **First letter: color of piece**
* **Second letter: exact piece**
* **Example**:
    * **`wK`: White King**

#### Pieces name
* **Pieces**:
    * **`K`: King (Король)**
    * **`Q`: Queen (Ферзь)**
    * **`R`: Rook (Ладья)**
    * **`B`: Bishop (Слон)**
    * **`N`: Knight (Конь)**
    * **`p`: Pawn (Пешка)**

### Class Player

* **Contain info about player**
* **There are two player -> _WHITE&BLACK_**  
#### Attributes
* `name`: **Full name of side**
* `letter`: **short name of side**
* `opposite`: **letter of enemy**

### Class Chess
* **Creates an application**
#### Attributes
* `pos` :
* `screen` : **Game screen**
* `font` : **Font initialization**
* `images` : **Pieces images**
* `running` : **The indicator of the program, if true, works, if false, ends**
* `WHITE` : **White player initialization**
* `BLACK` : **Black player initialization**
* `output` : ****Initializing the output of the game history on the right****
* `RATIO` : **Screen resolution**
* `DIMENSIONS` : **Board dimensions**
* `SQUARE_SIZE` : **Size of 1 square**
* `expand`: **The error for the screen resolution (so that the figures do not move out)**

#### Methods
* `_prepare_`: **Function that prepares an application for launch**
* `run`: **The main function for launching the application**

### Class Sound
* **Responsible for the sound operation in the program**

#### Attributes
* **This class does not have its own attributes, they are redefined in the chess class**

#### Methods
* `init`: **Initializes the sound system and all sounds**

### Class Graphics
* **The class responsible for the graphical component of the application**

#### Attributes
* `available_moves`: **List of available moves to show**
* `button_list`: **List of all buttons to show**
* `output_error`: **Information output shift** 
* `strings`: **List of information to show**

#### Methods
* `get_button_list`: **Create a list of buttons**
* `board_graphics`: **The main function for creating board and putting a pieces and showing available moves**
* `_board_`: **Draw a board**
* `_pieces_`: **Put a pieces on boards**
* `show_available_moves`: **Show all available moves from `available_moves`**
* `info_gainer`: **Receives information about the progress and generates information about it in a readable form**
* `print_info`:**Show information about turns**

### Class Controls
* **Inherits the `Chess` and `Sound` classes**
* **Responsible for user interaction with the program**
