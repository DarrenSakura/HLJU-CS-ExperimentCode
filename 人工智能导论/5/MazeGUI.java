import javax.swing.*;
import java.awt.*;
public class MazeGUI extends JFrame {
   private MazePanel mazePanel;
   public MazeGUI() {
       setTitle("A* 迷宫求解器");
       setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
       setLayout(new BorderLayout());
       // 创建迷宫面板
       mazePanel = new MazePanel();
       add(mazePanel, BorderLayout.CENTER);
       // 创建控制面板
       JPanel controlPanel = new JPanel();
       controlPanel.setLayout(new FlowLayout());
       JButton setStartBtn = new JButton("设置起点");
       JButton setEndBtn = new JButton("设置终点");
       JButton drawWallBtn = new JButton("绘制障碍");
       JButton eraseBtn = new JButton("擦除");
       JButton solveBtn = new JButton("求解路径");
       JButton clearBtn = new JButton("清空迷宫");
       // 按钮颜色标识
       setStartBtn.setBackground(new Color(255, 255, 150));
       setEndBtn.setBackground(new Color(255, 150, 150));
       drawWallBtn. setBackground(new Color(255, 150, 150));
       solveBtn.setBackground(new Color(150, 255, 150));
       // 添加按钮事件
       setStartBtn.addActionListener(e -> mazePanel.setMode(2));
       setEndBtn.addActionListener(e -> mazePanel.setMode(3));
       drawWallBtn.addActionListener(e -> mazePanel.setMode(1));
       eraseBtn.addActionListener(e -> mazePanel.setMode(0));
       solveBtn.addActionListener(e -> mazePanel.solveMaze());
       clearBtn.addActionListener(e -> mazePanel. clearMaze());
       controlPanel.add(setStartBtn);
       controlPanel.add(setEndBtn);
       controlPanel.add(drawWallBtn);
       controlPanel.add(eraseBtn);
       controlPanel. add(solveBtn);
       controlPanel.add(clearBtn);
       add(controlPanel, BorderLayout.SOUTH);
       // 添加说明面板
       JPanel infoPanel = new JPanel();
       infoPanel.setLayout(new BoxLayout(infoPanel, BoxLayout.Y_AXIS));
       infoPanel.setBorder(BorderFactory.createTitledBorder("使用说明"));
       infoPanel.add(new JLabel("1. 点击'设置起点'后在网格上点击设置起点（黄色）"));
       infoPanel.add(new JLabel("2. 点击'设置终点'后在网格上点击设置终点（红色）"));
       infoPanel.add(new JLabel("3. 点击'绘制障碍'后拖动鼠标绘制障碍（黑色）"));
       infoPanel.add(new JLabel("4. 点击'擦除'可以清除障碍"));
       infoPanel.add(new JLabel("5. 点击'求解路径'查看A*算法结果（绿色）"));
       add(infoPanel, BorderLayout.NORTH);
       pack();
       setLocationRelativeTo(null);
       setResizable(false);
   }
   public static void main(String[] args) {
       SwingUtilities.invokeLater(() -> {
           MazeGUI gui = new MazeGUI();
           gui.setVisible(true);
       });
   }
}
