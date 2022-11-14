package src;

import io.github.cdimascio.dotenv.Dotenv;

import java.sql.SQLException;
import java.util.HashMap;
import java.util.Scanner;

public class Generic  {
    public static final HashMap<Integer, Runnable> choices = new HashMap<>(
            8
    );
    public final static ExcelExporter excel = new ExcelExporter();
    public final static Scanner __input = new Scanner(System.in);
    public final static Dotenv dotenv = Dotenv.load();
    public static Database db;

    public static Object input(){return __input.nextLine();}

    public static Object input(String follow){
        Logger.water(follow);
        return input();
    }

    static {
        try {
            db = new Database(
                    dotenv.get("URL"),
                    dotenv.get("PORT"),
                    dotenv.get("DATABASE"),
                    true,
                    false,
                    dotenv.get("USER"),
                    dotenv.get("PASSWORD")
            );
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
