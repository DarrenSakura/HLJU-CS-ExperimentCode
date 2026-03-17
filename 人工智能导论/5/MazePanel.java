import javax. swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.List;
public class MazePanel extends JPanel {
   private int[][] maze;
   private int rows = 15;
   private int cols = 15;
   private int cellSize = 40;
   private Point start = null;
   private Point end = null;
   private List<Node> path = null;
   private static final int EMPTY = 0;
   private static final int WALL = 1;
   private static final int START = 2;
   private static final int END = 3;
   private int currentMode = WALL; // 当前绘制模式
   public MazePanel() {
       maze = new int[rows][cols];
       initializeMaze();
       setPreferredSize(new Dimension(cols * cellSize, rows * cellSize));
       setBackground(Color.WHITE);
       // 添加鼠标监听器
       addMouseListener(new MouseAdapter() {
           @Override
           public void mousePressed(MouseEvent e) {
               handleMouseClick(e.getX(), e.getY());
           }
       });
       addMouseMotionListener(new MouseMotionAdapter() {
           @Override
           public void mouseDragged(MouseEvent e) {
               handleMouseClick(e.getX(), e.getY());
           }
       });
   }
   private void initializeMaze() {
       // 初始化为空迷宫
       for (int i = 0; i < rows; i++) {
           for (int j = 0; j < cols; j++) {
               maze[i][j] = EMPTY;
           }
       }
   }
   private void handleMouseClick(int mouseX, int mouseY) {
       int col = mouseX / cellSize;
       int row = mouseY / cellSize;
       if (row >= 0 && row < rows && col >= 0 && col < cols) {
           if (currentMode == START) {
               if (start != null) {
                   maze[start.x][start.y] = EMPTY;
               }
               start = new Point(row, col);
               maze[row][col] = START;
           } else if (currentMode == END) {
               if (end != null) {
                   maze[end.x][end. y] = EMPTY;
               }
               end = new Point(row, col);
               maze[row][col] = END;
           } else if (currentMode == WALL) {
               if (maze[row][col] != START && maze[row][col] != END) {
                   maze[row][col] = WALL;
               }
           } else if (currentMode == EMPTY) {
               if (maze[row][col] == WALL) {
                   maze[row][col] = EMPTY;
               }
           }
           path = null; // 清除之前的路径
           repaint();
       }
   }
   public void setMode(int mode) {
       this.currentMode = mode;
   }
   public void clearMaze() {
       initializeMaze();
       start = null;
       end = null;
       path = null;
       repaint();
   }
   public void solveMaze() {
       if (start == null || end == null) {
           JOptionPane.showMessageDialog(this, "请先设置起点和终点！");
           return;
       }
       // 创建临时迷宫数组用于A*算法
       int[][] tempMaze = new int[rows][cols];
       for (int i = 0; i < rows; i++) {
           for (int j = 0; j < cols; j++) {
               tempMaze[i][j] = (maze[i][j] == WALL) ? 1 : 0;
           }
       }
       AStar aStar = new AStar(tempMaze);
       path = aStar.findPath(start.x, start.y, end.x, end.y);
       if (path == null) {
           JOptionPane.showMessageDialog(this, "没有找到路径！");
       }
       repaint();
   }
   @Override
   protected void paintComponent(Graphics g) {
       super.paintComponent(g);
       Graphics2D g2d = (Graphics2D) g;
       // 绘制网格和单元格
       for (int i = 0; i < rows; i++) {
           for (int j = 0; j < cols; j++) {
               int x = j * cellSize;
               int y = i * cellSize;
               // 绘制单元格背景
               if (maze[i][j] == WALL) {
                   g2d.setColor(Color. BLACK);
                   g2d. fillRect(x, y, cellSize, cellSize);
               } else if (maze[i][j] == START) {
                   g2d.setColor(Color. YELLOW);
                   g2d. fillRect(x, y, cellSize, cellSize);
               } else if (maze[i][j] == END) {
                   g2d.setColor(Color.RED);
                   g2d. fillRect(x, y, cellSize, cellSize);
               } else {
                   g2d.setColor(Color.WHITE);
                   g2d.fillRect(x, y, cellSize, cellSize);
               }
               // 绘制网格线
               g2d.setColor(Color. GRAY);
               g2d.drawRect(x, y, cellSize, cellSize);
           }
       }
       // 绘制路径
       if (path != null && path.size() > 0) {
           g2d.setColor(new Color(0, 200, 0)); // 绿色路径
           for (int i = 1; i < path.size() - 1; i++) {
               Node node = path.get(i);
               int x = node.y * cellSize;
               int y = node.x * cellSize;
               g2d.fillRect(x, y, cellSize, cellSize);
               // 重新绘制网格线
               g2d. setColor(Color.GRAY);
               g2d.drawRect(x, y, cellSize, cellSize);
               g2d.setColor(new Color(0, 200, 0));
           }
       }
   }
}