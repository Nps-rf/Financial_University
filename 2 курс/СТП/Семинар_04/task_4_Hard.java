import org.postgresql.util.PSQLException;
import src.Database;
import src.Generic;
import src.Logger;

import javax.ejb.Init;
import java.sql.*;
import java.util.UUID;


class task_3_Hard extends Generic {

    @Init
    private static void __main(){
        choices.put(1, () -> { try {SHOW_TABLES();} catch (SQLException e) {e.printStackTrace();}});
        choices.put(2, () -> { try {CREATE_TABLE();} catch (SQLException e) {e.printStackTrace();}});
        choices.put(3, () -> { try {task_3();} catch (SQLException e) {e.printStackTrace();}});
    }

    private static void task_3() throws SQLException {
        String s1 = (String) input("Строка: ");
        String sub = (String) input("Подстрока: ");
        op2sql(s1, sub);
        excel.export("task_03", db);
    }


    @SuppressWarnings("all")
    public static void main(String[] args) {
        __main(); // HASH-MAP INIT
        while (true)
            try {
                Logger.success("Выберите необходимую опцию:");
                Logger.water("\t1) Вывести все таблицы");
                Logger.water("\t2) Создать таблицу");
                Logger.water("\t3) Возвращение подстроки по индексам, результат сохранить в MySQL с последующим выводом в" +
                             "консоль.\n" +
                             "\t4. Перевод строк в верхний и нижний регистры, результат сохранить в MySQL с последующим выводом" +
                             "в консоль.\n" +
                             "\t5. Поиск подстроки и определение окончания подстроки, результат сохранить в MySQL с последующим" +
                             "выводом в консоль.\n" +
                             "\t6. Сохранить все данные (вышеполученные результаты) из MySQL в Excel и вывести на экран.");
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
            final String tablename = (String) input("Введите название базы данных");
            db.execute("create table " + tablename + "\n" +
                       "(\n" +
                       "    id       uuid not null\n" +
                       "        constraint " + tablename + "_pk\n" +
                       "            primary key,\n" +
                       "    string_1 text,\n" +
                       "    sub      text,\n" +
                       "    sub_ind  text,\n" +
                       "    low      text,\n" +
                       "    up       text,\n" +
                       "    contain  bool,\n" +
                       "    ends     bool\n" +
                       ");\n" +
                       "\n" +
                       "create unique index " + tablename + "_id_uindex\n" +
                       "    on " + tablename + " (id);\n");
        }
        catch (PSQLException e){
            System.out.println("Таблица создана");
        }

    }



    private static void op2sql(String s1, String s2) throws SQLException {
        final Connection con = db.getCon();
        final UUID uuid = UUID.randomUUID();
        String sql = """
                INSERT INTO task_03 (id, string_1, sub, sub_ind, low, up, contain, ends)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """;
        PreparedStatement preparedStatement = con.prepareStatement(sql);
        preparedStatement.setObject(1, uuid);
        preparedStatement.setString(2, s1);
        preparedStatement.setObject(3, s2);
        preparedStatement.setObject(4, s1.substring(5, 10));
        preparedStatement.setObject(5, s1.toLowerCase());
        preparedStatement.setObject(6, s1.toUpperCase());
        preparedStatement.setObject(7, s1.contains(s2));
        preparedStatement.setObject(8, s1.endsWith(s2));
        preparedStatement.executeUpdate();
        Logger.success("Успешно!");
    }


}

