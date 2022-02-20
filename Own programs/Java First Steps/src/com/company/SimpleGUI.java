package com.company;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;


public class SimpleGUI extends JFrame{
    private final JTextField Text = new JTextField("Write here", 10);
    private final JRadioButton radioButton1 = new JRadioButton("Select this");
    private final JCheckBox checkBox = new JCheckBox("Check", false);

    public SimpleGUI () {
        super("Simple Example");
        this.setBounds(100, 100, 300, 125);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        Container container = this.getContentPane();
        container.setLayout(new GridLayout(3, 3, 2, 2));
        JLabel label = new JLabel("Input:");
        container.add(label);
        container.add(Text);

        ButtonGroup group = new ButtonGroup();
        group.add(radioButton1);
        // Add to container
        container.add(radioButton1);
        container.add(radioButton1);
        JButton button = new JButton("Press me");
        button.addActionListener(new ButtonEventListener());
        container.add(button);
    }

    class ButtonEventListener implements ActionListener {
        public void actionPerformed(ActionEvent event) {
            String message = "Message was pressed\nText is " + Text.getText() + "\n";
            message += (radioButton1.isSelected() ? "Radio 1 " : "Radio 2 ") + "is selected\n";
            message += "Checkbox is " + ((checkBox.isSelected()) ? "checked" : "unchecked");
            JOptionPane.showMessageDialog(null, message, "Info", JOptionPane.PLAIN_MESSAGE);
        }
    }

}
