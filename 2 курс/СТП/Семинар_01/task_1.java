import io.github.cdimascio.dotenv.Dotenv;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashMap;

public class task_1 {

    HashMap<Object, Object> choices = new HashMap<>(); // TODO


    final static Dotenv dotenv = Dotenv.load();
    static Database db;

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

    public static void main(String[] args) throws SQLException {
        try{
        Logger.success("Выберите необходимую опцию:");
        Logger.water("\t1) Вывести все таблицы");
        SHOW_TABLES();
        }


        catch (Exception e){
            Logger.error("Произошла непредвиденная ошибка:");
            e.printStackTrace();
        }

    }

    public static void SHOW_TABLES() throws SQLException {
        ResultSet rs = db.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public'");
        Database.Utils.print_result(rs);
    }
}

