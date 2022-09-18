public final class Logger {

    public static void success(String sc_message) {
        System.out.println((char)27 + "[32m" + sc_message + (char)27 + "[0m");
    }

    public static void error(String err_message) {
        System.out.println((char)27 + "[31m" + err_message + (char)27 + "[0m");
    }

    public static void water(String err_message) {
        System.out.println((char)27 + "[34m" + err_message + (char)27 + "[0m");
    }

}
