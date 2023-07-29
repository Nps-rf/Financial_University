package main

import "fmt"

const (
	Player1Literal rune = 'X'
	Player2Literal rune = 'O'
	EmptyCell      rune = '□'
)

type Game struct {
	board       Board
	currentUser User
	turn        int8
}

type User struct {
	literal rune
}

type Board [3][3]rune

type GameError string

func (e GameError) Error() string {
	return string(e)
}

func NewGame() *Game {
	return &Game{
		board: Board{
			{EmptyCell, EmptyCell, EmptyCell},
			{EmptyCell, EmptyCell, EmptyCell},
			{EmptyCell, EmptyCell, EmptyCell},
		},
		currentUser: User{
			literal: Player1Literal,
		},
		turn: 0,
	}
}

func (g *Game) checkWin(player rune) bool {
	winSequences := [8][3][2]int{
		{{0, 0}, {0, 1}, {0, 2}},
		{{1, 0}, {1, 1}, {1, 2}},
		{{2, 0}, {2, 1}, {2, 2}},
		{{0, 0}, {1, 0}, {2, 0}},
		{{0, 1}, {1, 1}, {2, 1}},
		{{0, 2}, {1, 2}, {2, 2}},
		{{0, 0}, {1, 1}, {2, 2}},
		{{0, 2}, {1, 1}, {2, 0}},
	}
	for _, seq := range winSequences {
		if g.board[seq[0][0]][seq[0][1]] == player && g.board[seq[1][0]][seq[1][1]] == player && g.board[seq[2][0]][seq[2][1]] == player {
			return true
		}
	}
	return false
}

func (g *Game) assertValidMove(x, y int) error {
	if x < 1 || x > 3 || y < 1 || y > 3 {
		return GameError("Move out of range")
	} else if g.board[x-1][y-1] != EmptyCell {
		return GameError("Incorrect move")
	}
	return nil
}

func (g *Game) showBoard() {
	fmt.Println("   1  2  3")
	for i := 0; i < 3; i++ {
		fmt.Printf("%d ", i+1)
		for j := 0; j < 3; j++ {
			fmt.Printf(" %c ", g.board[i][j])
		}
		fmt.Println()
	}
}

func main() {
	game := NewGame()

	fmt.Println("Welcome to the Tik-Tak-Toe game!")

	for {
		game.showBoard()

		fmt.Printf("%c's player move:\n", game.currentUser.literal)

		var turnX = -1
		var turnY = -1

		_, err := fmt.Scanln(&turnX, &turnY)
		if err != nil {
			fmt.Println("User input error:", err)
			return
		}
		err = game.assertValidMove(turnX, turnY)
		if err != nil {
			fmt.Println(err)
			continue
		}
		game.board[turnX-1][turnY-1] = game.currentUser.literal

		if game.checkWin(game.currentUser.literal) {
			fmt.Printf("%c wins!", game.currentUser.literal)
			return
		}

		game.turn++
		if game.turn%2 == 0 {
			game.currentUser.literal = Player1Literal
		} else {
			game.currentUser.literal = Player2Literal
		}
	}
}
