import java.util.Scanner;

import static java.lang.System.exit;
import static java.lang.System.in;

public class Tic_Tac_Toe {
    protected static char[][] field = {
            {'☐', '☐', '☐'},
            {'☐', '☐', '☐'},
            {'☐', '☐', '☐'},
    };
    static char current_player = 'X';

    public static void main(String[] args) {
        //noinspection InfiniteLoopStatement
        while (true) run();
    }

    private static void run() {
        System.out.println("\033[93m" + "Current player: " + current_player + "\033[0m");
        draw_field();
        int x = input('x');
        int y = input('y');
        make_turn(x, y, current_player);
        if (isWin(current_player)){
            System.out.println("\033[92m" + current_player + " WON!" + "\033[0m");
            draw_field();
            exit(0);
        }
        switch_player();
        System.out.print("\n");
        sleep();
    }

    private static boolean isWin(char current_player) {
        for (char[] row : field){  // row checker
            if (isEqual(row, current_player)) return true;
        }
        for (int y = 0; y < 3; y++ ) {  // column checker
            char[] array = new char[3];
            for (int x = 0; x < 3; x++ ) array[x] = field[x][y];
            if (isEqual(array, current_player)) return true;
        }

        char[] array = new char[3];
        for (int x = 0; x < 3; x++ ) array[x] = field[x][x];  // column checker


        if (isEqual(array, current_player)) return true;

        array = new char[3];
        for (int x = 0; x < 3; x++ ) array[x] = field[x][(field.length - 1) - x];
        return isEqual(array, current_player);
    }

    private static void sleep() {
        try
        {
            Thread.sleep(500);
        }
        catch(InterruptedException ex)
        {
            Thread.currentThread().interrupt();
        }
    }

    private static void switch_player() {
        if (current_player == 'X')
        {
            current_player = 'O';
        }
        else current_player = 'X';
    }

    private static void make_turn(int x, int y, char current) {
        field[x - 1][y - 1] = current;
    }

    private static void draw_field() {
        System.out.println("  1 2 3");
        for (int row = 0; row < 3; row++) {
            System.out.print(row + 1 + " ");
            for (int column = 0; column < 3; column++) {
                System.out.print(field[row][column] + " ");
            }
            System.out.println();
        }
    }

    static int input(char variable) {
        while (true) {
            try {
                System.out.print("Input " + variable + ": ");
                int number = new Scanner(in).nextInt();
                if (0 <= number & number <= 3) {
                    return number;
                }
                else System.out.println("\033[91m" + "Number is out of range!" + "\033[0m");
            }
            catch (java.util.InputMismatchException wrong_value_e) {
                System.out.println("\033[91m" + "Not a number!" + "\033[0m");
            }
        }
    }
    private static boolean isEqual(char [] array, char equal_TO){
        for (char state : array){
            if (state != equal_TO){
                return false;
            }
        }
        return true;
    }
}
