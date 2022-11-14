import org.postgresql.util.PSQLException;
import src.ArrayPI;
import src.Database;
import src.Generic;
import src.Logger;

import javax.ejb.Init;
import java.sql.*;
import java.util.UUID;


    class task_6_Hard extends Generic {

        @Init
        private static void __main(){
            choices.put(1, () -> { try {SHOW_TABLES();} catch (SQLException e) {e.printStackTrace();}});
            choices.put(2, () -> { try {CREATE_TABLE();} catch (SQLException e) {e.printStackTrace();}});
            choices.put(3, () -> { try {task_3();} catch (SQLException e) {e.printStackTrace();}});
        }

        private static void task_3() throws SQLException {
            Matrix a = new Matrix(2, 2);
            ArrayPI.show(a.Array1);
            ArrayPI.show(a.Array2);
            ArrayPI.show(a.result);
            op2sql(a.Array1, a.Array2, a.result);
            excel.export("task_06", db);
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
                           "    id     uuid not null\n" +
                           "        constraint " + tablename + "pk\n" +
                           "            primary key,\n" +
                           "    array1 int[][],\n" +
                           "    array2 int[][],\n" +
                           "    res    int[][]\n" +
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



        private static void op2sql(int[][] s1, int[][] s2, int[][] res) throws SQLException {
            final Connection con = db.getCon();
            final UUID uuid = UUID.randomUUID();
            String sql = """
                INSERT INTO task_06 (id, array1, array2, res) VALUES (?, ?, ?, ?);
                """;
            PreparedStatement preparedStatement = con.prepareStatement(sql);
            preparedStatement.setObject(1, uuid);
            preparedStatement.setObject(2, s1);
            preparedStatement.setObject(3, s2);
            preparedStatement.setObject(4, res);
            preparedStatement.executeUpdate();
            Logger.success("Успешно!");
        }


    }

