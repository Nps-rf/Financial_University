import org.postgresql.util.PSQLException;
import src.Database;
import src.Generic;
import src.Logger;

import javax.ejb.Init;
import java.sql.*;
import java.util.UUID;


class task_2_Hard extends Generic {

    @Init
    private static void __main(){
        choices.put(1, () -> { try {SHOW_TABLES();} catch (SQLException e) {e.printStackTrace();}});
        choices.put(2, () -> { try {CREATE_TABLE();} catch (SQLException e) {e.printStackTrace();}});
        choices.put(3, () -> { try {task_3();} catch (SQLException e) {e.printStackTrace();}});
    }

    private static void task_3() throws SQLException {
        String s1 = (String) input();
        String s2 = (String) input();
        op2sql(s1, s2);
        excel.export("task_02", db);
    }


    @SuppressWarnings("all")
    public static void main(String[] args) {
        __main(); // HASH-MAP INIT
        while (true)
        try {
            Logger.success("Выберите необходимую опцию:");
            Logger.water("\t1) Вывести все таблицы");
            Logger.water("\t2) Создать таблицу");
            Logger.water("\t3) Ввести две строки с клавиатуры, результат сохранить в MySQL с последующим выводом в консоль. " +
                         "\n\t4. Подсчитать размер ранее введенных строк, результат сохранить в MySQL с последующим выводом в " +
                         "консоль. " +
                         "\n\t5. Объединить две строки в единое целое, результат сохранить в MySQL с последующим выводом в " +
                         "консоль. " +
                         "\n\t6. Сравнить две ранее введенные строки, результат сохранить в MySQL с последующим выводом в " +
                         "консоль. " +
                         "\n\t7. Сохранить все данные (вышеполученные результаты) из MySQL в Excel и вывести на экран.");
            int choice = Integer.parseInt((String) input()); // Scans the next token of the input as an int.
            choices.get(choice).run();
        } catch (Exception e) {
            Logger.error("Произошла непредвиденная ошибка:");
            e.printStackTrace();
        }
    }

    @SuppressWarnings("all")
    public static void SHOW_TABLES() throws SQLException {
        final ResultSet rs = db.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public'");
        Database.Utils.print_result(rs);
    }
    @SuppressWarnings("all")
    public static void CREATE_TABLE() throws SQLException {
        try {
            db.execute("create table task_03\n" +
                       "(\n" +
                       "    id          uuid not null\n" +
                       "        constraint task_03_pk\n" +
                       "            primary key,\n" +
                       "    string_1    text,\n" +
                       "    string_2    text,\n" +
                       "    size_1      integer,\n" +
                       "    size_2      integer,\n" +
                       "    concat      text,\n" +
                       "    is_equal    boolean,\n" +
                       "    executed_at timestamp\n" +
                       ");\n" +
                       "\n" +
                       "alter table task_03\n" +
                       "    owner to nps_rf;\n" +
                       "\n" +
                       "create unique index task_03_id_uindex\n" +
                       "    on task_03 (id);\n" +
                       "\n");
        }
        catch (PSQLException e){
            System.out.println("Таблица создана");
        }

    }



    private static void op2sql(String s1, String s2) throws SQLException {
        final Connection con = db.getCon();
        final UUID uuid = UUID.randomUUID();
        final Timestamp timestamp = new Timestamp(System.currentTimeMillis());
        String sql = """
                INSERT INTO task_02 (id, string_1, string_2, size_1, size_2, concat, is_equal, executed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """;
        PreparedStatement preparedStatement = con.prepareStatement(sql);
        preparedStatement.setObject(1, uuid);
        preparedStatement.setString(2, s1);
        preparedStatement.setString(3, s2);
        preparedStatement.setObject(4, s1.length());
        preparedStatement.setObject(5, s2.length());
        preparedStatement.setObject(6, s1.concat(s2));
        preparedStatement.setObject(7, s1.equals(s2));
        preparedStatement.setObject(8, timestamp);
        preparedStatement.executeUpdate();
        Logger.success("Успешно!");
    }


}

