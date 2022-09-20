package src;

import java.io.PrintStream;
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;
import java.util.Arrays;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class calculator {

    /**
     * Вариант, без тернарного оператора, здесь нужно немного подумать.
     * @param expression выражение для расчета
     * @param args хитрость, до которой стоит догадаться
     */
    public static Object calc(String expression, Object ... args) {
        try {
            // 1. Отображаем результат
            return BigDecimal.class.getMethod(
                    Arrays.asList("multiply", "add", "subtract", "divide").get(
                            // 3. Запоминаем все требуемые значения в args и достаем код операции
                            (Integer) (args = new Object[] {args = new Object[] {
                                    Pattern.compile("([+-]?(?:\\d+(?:\\.\\d*)?|\\.\\d+)(?:[eE][+-]?\\d+)?)\\s*([+-\\\\*/])\\s*([+-]?(?:\\d+(?:\\.\\d*)?|\\.\\d+)(?:[eE][+-]?\\d+)?)$").
                                            matcher(expression)}, args[0], ((Matcher) args[0]).find(), ((Matcher) args[0]).group(1), ((int) ((Matcher) args[0]).group(2).charAt(0) -41) / 2,
                                    ((Matcher) args[0]).group(3)})[4]),
                    // 4. Вычисляем результат
                    BigDecimal.class, MathContext.class).invoke(
                    // 5. Первый аргумент пошел
                    new BigDecimal(args[3].toString()),
                    // 6. Второй аргумент пошел
                    new BigDecimal(args[5].toString()), new MathContext(10, RoundingMode.HALF_EVEN));
        } catch (Exception ex) {
            /** Хитрый трюк сказать пользователю что выражение фиговое */
            try (PrintStream stream = (System.out.append("Nan"))) {}
        }
        return null;
    }

    public static void main(String[] args) {
        calc("+5 + -12");
        calc("+5 * -12");
        calc("+5 - -12");
        calc("+5 / -12");
    }
}