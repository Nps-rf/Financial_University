import org.postgresql.util.PSQLException;
import src.Database;
import src.Logger;
import src.calculator;

import javax.ejb.Init;
import java.sql.*;
import java.util.Objects;
import java.util.UUID;


class task_1_Medium extends Generic{

    @Init
    private static void __main(){
        choices.put(1, () -> { try {SHOW_TABLES();} catch (SQLException e) {e.printStackTrace();}});
        choices.put(2, () -> { try {CREATE_TABLE();} catch (SQLException e) {e.printStackTrace();}});
        choices.put(3, task_1_Medium::calculate);
        choices.put(4, () -> { try {calculate_SQL();} catch (SQLException e) {e.printStackTrace();}});
        choices.put(5, task_1_Medium::extended_calculator);
        choices.put(6, task_1_Medium::extended_calculator);
    }
    @SuppressWarnings("all")
    public static void main(String[] args) {
        __main(); // HASH-MAP INIT
        while (true)
            try {
            Logger.success("Выберите необходимую опцию:");
            Logger.water("\t1) Вывести все таблицы");
            Logger.water("\t2) Создать таблицу");
            Logger.water("\t3) Посчитать выражение (Базовые арифметические операции)");
            Logger.water("\t4) Посчитать выражение (Базовые арифметические операции) и записать его в БД");
            Logger.water("\t5) Посчитать выражение (Расширенные арифметические операции)");
            Logger.water("\t6) Посчитать выражение (Расширенные арифметические операции) и записать его в бд");
            int choice = Integer.parseInt((String) input()); // Scans the next token of the input as an int.
            choices.get(choice).run();
            System.out.println();
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
        db.execute("create table if not exists" + tablename +
                "(" +
                "    id            uuid        not null" +
                "        constraint " + tablename + "_pk" +
                "            primary key," +
                "    example       varchar(64) not null," +
                "    result        bigint      not null," +
                "    hint          text," +
                "    time_executed timestamp" +
                ");" +
                "" +
                "alter table \t" + tablename +
                "    owner to nps_rf;" +
                "" +
                "create unique index " + tablename + "_id_uindex" +
                "    on " + tablename + " (id);");
        }
        catch (PSQLException e){
            System.out.println("Таблица создана");
        }

    }

    public static void calculate() {
        Logger.success(Objects.requireNonNull(calculator.calc((String) input("Введите ваше выражение:\nВНИМАНИЕ! Поддерживается только два аргумента операции "))).toString());
    }

    @SuppressWarnings("all")
    public static void extended_calculator(){
        Logger.success("Выберите тип данных:");
        Logger.water("\t1) Integer");
        Logger.water("\t2) Float");
        String dtype = (String) input();
        if (Objects.equals(dtype, "1")){
            int arg_1 = Integer.parseInt((String) input("Введите первый аргумент"));
            int arg_2 = Integer.parseInt((String) input("Введите второй аргумент"));
            Logger.success("Выберите операцию:");
            Logger.water("\t1) Возведение в степень");
            Logger.water("\t2) Остаток от деления");
            String op = (String) input();

            if (Objects.equals(op, "1")){
                Logger.success(String.valueOf(Math.pow(arg_1, arg_2)));
            }
            else if (Objects.equals(op, "2")){
                Logger.success(String.valueOf(arg_1 % arg_2));
            }


        }
        else {
            Float arg_1 = (Float) input("Введите первый аргумент");
            Float arg_2 = (Float) input("Введите второй аргумент");
            Logger.success("Выберите операцию:");
            Logger.water("\t1) Возведение в степень");
            Logger.water("\t2) Остаток от деления");
            String op = (String) input();

            if (Objects.equals(op, "1")){
                Logger.success(String.valueOf(Math.pow(arg_1, arg_2)));
            }
            else if (Objects.equals(op, "2")){
                Logger.success(String.valueOf(arg_1 % arg_2));
            }
        }
    }

    public static void calculate_SQL() throws SQLException {
        final String example = (String) input("Введите ваше выражение:\nВНИМАНИЕ! Поддерживается только два аргумента операции ");
        final String res = Objects.requireNonNull(calculator.calc(example)).toString();
        op2sql(example, res);
    }

    private static void op2sql(String example, String res) throws SQLException {
        final Connection con = db.getCon();
        final UUID uuid = UUID.randomUUID();
        final Timestamp timestamp = new Timestamp(System.currentTimeMillis());
        String sql = """
                INSERT INTO task_01 (id, example, result, time_executed)
                VALUES (?, ?, ?, ?);
                """;
        PreparedStatement preparedStatement = con.prepareStatement(sql);
        preparedStatement.setObject(1, uuid);
        preparedStatement.setString(2, example);
        preparedStatement.setString(3, res);
        preparedStatement.setObject(4, timestamp);
        Logger.success(res);
        preparedStatement.executeUpdate();
        Logger.success("Успешно!");
    }

}

