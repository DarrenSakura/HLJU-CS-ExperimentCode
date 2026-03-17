public class Node implements Comparable<Node> {
   public int x, y;
   public int g; // 从起点到当前节点的实际代价
   public int h; // 从当前节点到终点的启发式估计代价
   public int f; // f = g + h
   public Node parent;
   public Node(int x, int y) {
       this.x = x;
       this.y = y;
       this.g = 0;
       this.h = 0;
       this.f = 0;
       this.parent = null;
   }
   @Override
   public int compareTo(Node other) {
       return Integer.compare(this.f, other.f);
   }
   @Override
   public boolean equals(Object obj) {
       if (this == obj) return true;
       if (obj == null || getClass() != obj.getClass()) return false;
       Node node = (Node) obj;
       return x == node.x && y == node.y;
   }
   @Override
   public int hashCode() {
       return 31 * x + y;
   }
}