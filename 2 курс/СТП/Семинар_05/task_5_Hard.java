import org.postgresql.util.PSQLException;
import src.Database;
import src.Generic;
import src.Logger;

import javax.ejb.Init;
import java.sql.*;
import java.util.UUID;


class task_5_Hard extends Generic {

    @Init
    private static void __main(){
        choices.put(1, () -> { try {SHOW_TABLES();} catch (SQLException e) {e.printStackTrace();}});
        choices.put(2, () -> { try {CREATE_TABLE();} catch (SQLException e) {e.printStackTrace();}});
        choices.put(3, () -> { try {task_3();} catch (SQLException e) {e.printStackTrace();}});
    }

    private static void task_3() throws SQLException {
        String s1 = (String) input("Строка 1: ");
        String s2 = (String) input("Строка 2: ");
        StringBuffer sbuffer1 = new StringBuffer();
        StringBuffer sbuffer2 = new StringBuffer();
        sbuffer1.append(s1);
        sbuffer2.append(s2);
        op2sql(sbuffer1, sbuffer2);
        excel.export("task_05", db);
    }


    @SuppressWarnings("all")
    public static void main(String[] args) {
        __main(); // HASH-MAP INIT
        while (true)
            try {
                Logger.success("Выберите необходимую опцию:");
                Logger.water("\t1. Вывести все таблицы из MySQL.\n" +
                             "\t2. Создать таблицу в MySQL.\n" +
                             "\t3. Сделать чтобы работало.");
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
                       "    id        uuid not null\n" +
                       "        constraint " + tablename + "_pk\n" +
                       "            primary key,\n" +
                       "    string_1  varchar(16),\n" +
                       "    string_2  varchar(16),\n" +
                       "    reverse_1 varchar(16),\n" +
                       "    reverse_2 varchar(16),\n" +
                       "    concat_1  varchar(16),\n" +
                       "    concat_2  varchar(16)\n" +
                       ");\n" +
                       "\n" +
                       "create unique index " + tablename + "_id_uindex\n" +
                       "    on " + tablename + " (id);\n" +
                       "\n");
        }
        catch (PSQLException e){
            System.out.println("Таблица создана");
        }

    }



    private static void op2sql(StringBuffer s1, StringBuffer s2) throws SQLException {
        final Connection con = db.getCon();
        final UUID uuid = UUID.randomUUID();
        String sql = """
                INSERT INTO task_05 (id, string_1, string_2, reverse_1, reverse_2, concat_1, concat_2)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """;
        String reverse_1 = new StringBuilder(s1).reverse().toString();
        String reverse_2 = new StringBuilder(s2).reverse().toString();

        String concat_1 = s1.toString().concat(s2.toString());
        String concat_2 = s2.toString().concat(s1.toString());
        PreparedStatement preparedStatement = con.prepareStatement(sql);
        preparedStatement.setObject(1, uuid);
        preparedStatement.setObject(2, s1.toString());
        preparedStatement.setObject(3, s2.toString());
        preparedStatement.setObject(4, reverse_1);
        preparedStatement.setObject(5, reverse_2);
        preparedStatement.setObject(6, concat_1);
        preparedStatement.setObject(7, concat_2);
        preparedStatement.executeUpdate();
        Logger.success("Успешно!");
    }


}

