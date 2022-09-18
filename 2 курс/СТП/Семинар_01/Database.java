import java.sql.*;

public final class Database {
    Connection _con;

    // Missing implementation exactly for database object
    public Database(
            String url, // Database URL (localhost, 192.168.0.1)
            String port, // MySQL Default -> 5433
            String database, // Database name (test?)
            Boolean autoReconnect, // Use reconnection?
            Boolean useSSL, // Use SSL?
            String user,
            String password
    ) throws SQLException {
        this._con = DriverManager.getConnection(
                "jdbc:postgresql://" + url + ":" + port + "/" + database + "?autoReconnect=" +
                        autoReconnect.toString() + "&useSSL=" + useSSL.toString(),
                user,
                password
        );
    }

    /**
     * @param sql your query that you need to execute, SHOW TABLES, INSERT INTO ... VALUES ...
     * @return result of query
     */
    public ResultSet execute(String sql) throws SQLException {
        Statement stmt = this._con.createStatement();
        return stmt.executeQuery(sql);
    }


    public static final class Utils {
        public static void print_result(ResultSet result) throws SQLException {
            while (result.next()) {
                System.out.println(result.getString(1));
            }
        }
    }

}