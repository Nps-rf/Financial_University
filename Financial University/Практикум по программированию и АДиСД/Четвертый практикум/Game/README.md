<img src="https://cdn1.iconfinder.com/data/icons/filled-line-christmas-icons/75/_deer-256.png" align="right"/>


# ♛ Chess game ♛
____
![Python version](https://img.shields.io/badge/Python-3.8-blue)
![Pygame version](https://img.shields.io/badge/Pygame-2.0.1-blueviolet)
![Project status](https://img.shields.io/badge/Status-WIP-red)

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
* **This class does not have its own attributes, they are redefined in the `Chess` class**

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

#### Attributes
* `available`: **List of available moves for chosen piece**
* `history`: **Game history**
* `old_piece`: **Piece that was chosen before**
* `row`: **Calculated coordinate along the ordinate axis**
* `column`: **Calculated coordinate along the abscissa axis**
* `current_player`: **The player making the move**
* `chose`: **Is the shape selected or not**
* `piece`: **An array where the first value is the shape, and the second is its coordinates**
* `x`: **The coordinate of the click on the abscissa axis**
* `y`: **The coordinate of the click on the ordinate axis**

#### Methods
* `run_contols`: **Allow user to interact with program**
* `_look4click_`: **Checks whether the user clicked on the cross (or other place) and interact with program.**

### Class Rules
* **Contain methods that find available moves for pieces, also looking for checkmate**

#### Attributes
* **This class does not have its own attributes**

#### Methods
* `pawn`: **Find available moves for pawn**
* `knight`: **Find available moves for knight**
* `bishop`: **Find available moves for bishop**
* `rook`: **Find available moves for rook**
* `queen`: **Find available moves for queen**
* `king`: **Find available moves for king**

## Illustrations
### Move
![](https://psv4.userapi.com/c534536/u43923203/docs/d11/5ce302774984/Untitledd.gif?extra=kCTPlEOFhdcgKL0k1Qo1FYss9P35QUddpDoM51VMPG__Zr4Ni5EraQ1LUi7T2hHmJKOdQc-GEhxVcF7Eb7YKj19G0oAm3iKrHIROJs6ME-lBet0oE4lFhaZOQpQ92w9Pn1CI0zBUg5dBSwUoLDVX)
### Beat
![](https://psv4.userapi.com/c534536/u43923203/docs/d45/67ca656be87d/fdhgdfh.gif?extra=oowso8FC6i0UogZKRDSOLRLp7rNtRmjANHr5BYB2zH9pnUvr37EBC_3S3IS7RKohiosq81tTdwOGEGMmF5V_hixUoayKxsbDVC7FCmafwIR21OrUUfdb5Df_j7vwuq68MgJ1GhFTaJ1gbhb48QrY)
### Other figures
![](https://psv4.userapi.com/c240331/u43923203/docs/d17/9f58ca37cd6c/dfhgdghf.gif?extra=_ZxC06r_1Oh11DQodgNvYSQtmuaY6ltxfjVDaihz5DkjUUUGyCucMqOEH2ZXlOexnJYyA1hsJKofh2Jo3NsqPtHLaHW6vBiGlXrxa8RW_XwSmWB-0NuYtn8kWJ1_5FeA4ph7ErZIbFHU9--xltFC)
### Canceling moves
![](https://vk.com/doc43923203_624567497?hash=4a3018d699dd179316&dl=2dbb59912af7a44162&wnd=1&module=im)
