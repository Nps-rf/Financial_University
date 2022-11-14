package src;

import java.util.Arrays;

import static java.lang.Integer.parseInt;

public class ArrayPI {
    public int[][] Array1;
    public int[][] Array2;


    public ArrayPI(int x, int y) {
        Array1 = getMatrix(x, y);
        Array2 = getMatrix(x, y);
    }

    public static int[][] getMatrix(int x, int y) {
        int[][] Matrix1 = new int[x][y];

        for (int i = 0; i < Matrix1.length; i++)

            for (int j = 0; j < Matrix1[i].length; j++) {

                System.out.printf("[%d][%d]: ", i, j);
                Matrix1[i][j] = parseInt((String) Generic.input());

            }
        System.out.println();
        return Matrix1;
    }

    public static void show(int[][] Array){ System.out.println(Arrays.deepToString(Array)); }
}
