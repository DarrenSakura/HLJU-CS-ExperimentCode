import java.util.*;
public class AStar {
   private int[][] maze;
   private int rows;
   private int cols;
   // 四个方向：上、下、左、右
   private final int[][] directions = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
   public AStar(int[][] maze) {
       this.maze = maze;
       this.rows = maze.length;
       this.cols = maze[0].length;
   }
   // 计算曼哈顿距离作为启发函数
   private int heuristic(int x1, int y1, int x2, int y2) {
       return Math.abs(x1 - x2) + Math.abs(y1 - y2);
   }
   // 检查位置是否有效
   private boolean isValid(int x, int y) {
       return x>=0&&x<rows&&y>=0&&y<cols&&maze[x][y]!=1;
   }
   // A*算法寻路
   public List<Node>findPath(int startX,int startY,int endX,int endY){
       PriorityQueue<Node> openList = new PriorityQueue<>();
       Set<Node> closedList = new HashSet<>();
       Node startNode = new Node(startX, startY);
       Node endNode = new Node(endX, endY);
       startNode.g = 0;
       startNode.h = heuristic(startX, startY, endX, endY);
       startNode.f = startNode. g + startNode.h;
       openList.add(startNode);
       while (!openList.isEmpty()) {
           Node current = openList. poll();
           // 找到终点
           if (current.equals(endNode)) {
               return reconstructPath(current);
           }
           closedList.add(current);
           // 探索相邻节点
           for (int[] dir : directions) {
               int newX = current.x + dir[0];
               int newY = current.y + dir[1];
               if (! isValid(newX, newY)) {
                   continue;
               }
               Node neighbor = new Node(newX, newY);
               if (closedList.contains(neighbor)) {
                   continue;
               }
               int tentativeG = current.g + 1;
               boolean inOpenList = openList.contains(neighbor);
               if (!inOpenList || tentativeG < neighbor.g) {
                   neighbor.parent = current;
                   neighbor. g = tentativeG;
                   neighbor.h = heuristic(newX, newY, endX, endY);
                   neighbor.f = neighbor.g + neighbor.h;
                   
                   if (!inOpenList) {
                       openList.add(neighbor);
                   }
               }
           }
       }
       // 没有找到路径
       return null;
   }
   // 重建路径
   private List<Node> reconstructPath(Node endNode) {
       List<Node> path = new ArrayList<>();
       Node current = endNode;
       
       while (current != null) {
           path.add(current);
           current = current.parent;
       }
       Collections.reverse(path);
       return path;
   }
}