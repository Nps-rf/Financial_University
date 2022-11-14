import org.postgresql.util.PSQLException;
import src.Database;
import src.Generic;
import src.Logger;

import javax.ejb.Init;
import java.sql.*;
import java.util.UUID;


class task_3_Hard extends Generic {

    @Init
    private static void main(){
        choices.put(1, () -> { try {SHOW_TABLES();} catch (SQLException e) {e.printStackTrace();}});
        choices.put(2, () -> { try {CREATE_TABLE();} catch (SQLException e) {e.printStackTrace();}});
        choices.put(3, () -> { try {task_3();} catch (SQLException e) {e.printStackTrace();}});
    }

    private static void task_3() throws SQLException {
        Float s1 = Float.parseFloat((String) input("Число 1: "));
        Float s2 = Float.parseFloat((String) input("Число 2: "));
        op2sql(s1, s2);
        excel.export("task_04", db);
    }


    @SuppressWarnings("all")
    public static void main(String[] args) {
        main(); // HASH-MAP INIT
        while (true)
            try {
                Logger.success("Выберите необходимую опцию:");
                Logger.water("\t1. Вывести все таблицы из MySQL.\n" +
                             "\t2. Создать таблицу в MySQL.\n" +
                             "\t3. Выполнение задачи базового варианта, результат сохранить в MySQL с последующим выводом в консоль.\n" +
                             "\t4. Сохранить все данные (вышеполученные результаты) из MySQL в Excel и вывести на экран.");
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
                       "    id   uuid not null\n" +
                       "        constraint " + tablename + "_pk\n" +
                       "            primary key,\n" +
                       "    nums int[8],\n" +
                       "    odd  bool[8],\n" +
                       "    even bool[8]\n" +
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



    private static void op2sql(Float s1, Float s2) throws SQLException {
        final Connection con = db.getCon();
        final UUID uuid = UUID.randomUUID();
        String sql = """
                INSERT INTO task_04 (id, nums, odd, even)
                VALUES (?, ?, ?, ?);
                """;
        boolean[] odd = {s1 % 1 == 0, s2 % 1 == 0};
        boolean[] even = {s1 % 2 == 0, s2 % 2 == 0};
        PreparedStatement preparedStatement = con.prepareStatement(sql);
        preparedStatement.setObject(1, uuid);
        preparedStatement.setObject(2, new float[] {s1, s2});
        preparedStatement.setObject(3, odd);
        preparedStatement.setObject(4, even);
        preparedStatement.executeUpdate();
        Logger.success("Успешно!");
    }


}

