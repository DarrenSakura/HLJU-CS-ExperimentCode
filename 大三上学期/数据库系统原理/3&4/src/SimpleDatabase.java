import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.util.*;
import java.util.List;
import java.util.regex.*;

public class SimpleDatabase extends JFrame {
    private JTextArea sqlInput;
    private JTextArea outputArea;
    private JTable resultTable;
    private DefaultTableModel tableModel;
    private JScrollPane tableScrollPane;
    
    private Map<String, Database> databases = new HashMap<>();
    private Database currentDatabase = null;
    private static final String DATA_DIR = "database_data";
    
    public SimpleDatabase() {
        setTitle("模拟数据库管理系统");
        setSize(1000, 700);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout(10, 10));
        
        // 创建数据目录
        new File(DATA_DIR).mkdirs();
        
        // 加载已保存的数据库
        loadDatabases();
        
        // SQL输入区域
        JPanel topPanel = new JPanel(new BorderLayout(5, 5));
        topPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 5, 10));
        
        JLabel sqlLabel = new JLabel("SQL语句输入 (支持多行语句，每行一条):");
        sqlInput = new JTextArea(8, 50);
        sqlInput.setFont(new Font("Monospaced", Font.PLAIN, 12));
        JScrollPane sqlScrollPane = new JScrollPane(sqlInput);
        
        topPanel.add(sqlLabel, BorderLayout.NORTH);
        topPanel.add(sqlScrollPane, BorderLayout.CENTER);
        
        // 按钮面板
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JButton executeBtn = new JButton("执行SQL");
        JButton clearBtn = new JButton("清空输入");
        JButton clearOutputBtn = new JButton("清空输出");
        
        executeBtn.addActionListener(e -> executeSQL());
        clearBtn.addActionListener(e -> sqlInput.setText(""));
        clearOutputBtn.addActionListener(e -> {
            outputArea.setText("");
            tableModel.setRowCount(0);
            tableModel.setColumnCount(0);
        });
        
        buttonPanel.add(executeBtn);
        buttonPanel.add(clearBtn);
        buttonPanel.add(clearOutputBtn);
        topPanel.add(buttonPanel, BorderLayout.SOUTH);
        
        // 中间面板 - 结果显示
        JPanel centerPanel = new JPanel(new BorderLayout(5, 5));
        centerPanel.setBorder(BorderFactory.createEmptyBorder(5, 10, 5, 10));
        
        // 表格显示
        tableModel = new DefaultTableModel();
        resultTable = new JTable(tableModel);
        resultTable.setAutoResizeMode(JTable.AUTO_RESIZE_OFF);
        tableScrollPane = new JScrollPane(resultTable);
        tableScrollPane.setPreferredSize(new Dimension(900, 250));
        
        centerPanel.add(new JLabel("查询结果:"), BorderLayout.NORTH);
        centerPanel.add(tableScrollPane, BorderLayout.CENTER);
        
        // 输出信息区域
        JPanel bottomPanel = new JPanel(new BorderLayout(5, 5));
        bottomPanel.setBorder(BorderFactory.createEmptyBorder(5, 10, 10, 10));
        
        outputArea = new JTextArea(8, 50);
        outputArea.setEditable(false);
        outputArea.setFont(new Font("Monospaced", Font.PLAIN, 11));
        JScrollPane outputScrollPane = new JScrollPane(outputArea);
        
        bottomPanel.add(new JLabel("执行信息:"), BorderLayout.NORTH);
        bottomPanel.add(outputScrollPane, BorderLayout.CENTER);
        
        add(topPanel, BorderLayout.NORTH);
        add(centerPanel, BorderLayout.CENTER);
        add(bottomPanel, BorderLayout.SOUTH);
        
        setLocationRelativeTo(null);
        
        // 添加窗口关闭监听器，保存数据
        addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                saveDatabases();
            }
        });
    }
    
    private void loadDatabases() {
        File dataDir = new File(DATA_DIR);
        File[] files = dataDir.listFiles((dir, name) -> name.endsWith(".db"));
        if (files != null) {
            for (File file : files) {
                try {
                    ObjectInputStream ois = new ObjectInputStream(new FileInputStream(file));
                    Database db = (Database) ois.readObject();
                    databases.put(db.name, db);
                    ois.close();
                } catch (Exception e) {
                    System.err.println("加载数据库失败: " + file.getName());
                }
            }
        }
    }
    
    private void saveDatabases() {
        for (Database db : databases.values()) {
            try {
                File file = new File(DATA_DIR, db.name + ".db");
                ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(file));
                oos.writeObject(db);
                oos.close();
            } catch (Exception e) {
                System.err.println("保存数据库失败: " + db.name);
            }
        }
    }
    
    private void saveDatabase(String dbName) {
        if (databases.containsKey(dbName)) {
            try {
                File file = new File(DATA_DIR, dbName + ".db");
                ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(file));
                oos.writeObject(databases.get(dbName));
                oos.close();
            } catch (Exception e) {
                outputArea.append("保存数据库失败: " + e.getMessage() + "\n");
            }
        }
    }
    
    private void deleteDatabase(String dbName) {
        File file = new File(DATA_DIR, dbName + ".db");
        if (file.exists()) {
            file.delete();
        }
    }
    
    private void executeSQL() {
        String sqlText = sqlInput.getText().trim();
        if (sqlText.isEmpty()) {
            outputArea.append("错误: SQL语句不能为空\n");
            return;
        }
        
        // 分割多行SQL语句，支持分号结尾
        List<String> sqlStatements = new ArrayList<>();
        StringBuilder currentStatement = new StringBuilder();
        
        for (String line : sqlText.split("\n")) {
            line = line.trim();
            if (line.isEmpty() || line.startsWith("--") || line.startsWith("//")) {
                continue;
            }
            
            currentStatement.append(line).append(" ");
            
            // 如果行以分号结尾，这是一条完整的SQL语句
            if (line.endsWith(";")) {
                String sql = currentStatement.toString().trim();
                if (!sql.isEmpty()) {
                    sqlStatements.add(sql.substring(0, sql.length() - 1)); // 移除分号
                }
                currentStatement = new StringBuilder();
            }
        }
        
        // 处理最后一条没有分号的语句
        if (currentStatement.length() > 0) {
            String sql = currentStatement.toString().trim();
            if (!sql.isEmpty()) {
                sqlStatements.add(sql);
            }
        }
        
        int successCount = 0;
        int failCount = 0;
        
        outputArea.append("========== 开始执行 ==========\n");
        
        for (String sql : sqlStatements) {
            try {
                outputArea.append("\n> " + sql + "\n");
                String result = procesSQL(sql);
                outputArea.append(result + "\n");
                successCount++;
            } catch (Exception e) {
                outputArea.append("错误: " + e.getMessage() + "\n");
                e.printStackTrace();
                failCount++;
            }
        }
        
        outputArea.append("\n========== 执行完成 ==========\n");
        outputArea.append("成功: " + successCount + " 条, 失败: " + failCount + " 条\n\n");
        
        // 自动滚动到底部
        outputArea.setCaretPosition(outputArea.getDocument().getLength());
    }
    
    private String procesSQL(String sql) {
        sql = sql.trim();
        String sqlLower = sql.toLowerCase();
        
        if (sqlLower.startsWith("create database")) {
            return createDatabase(sql);
        } else if (sqlLower.startsWith("drop database")) {
            return dropDatabase(sql);
        } else if (sqlLower.startsWith("use")) {
            return useDatabase(sql);
        } else if (sqlLower.equals("return")) {
            return "执行完成";
        } else if (sqlLower.startsWith("create table")) {
            return createTable(sql);
        } else if (sqlLower.startsWith("insert into")) {
            return insertInto(sql);
        } else if (sqlLower.startsWith("delete from")) {
            return deleteFrom(sql);
        } else if (sqlLower.startsWith("select")) {
            return select(sql);
        } else {
            return "不支持的SQL语句类型";
        }
    }
    
    private String createDatabase(String sql) {
        Pattern p = Pattern.compile("create\\s+database\\s+(\\w+)", Pattern.CASE_INSENSITIVE);
        Matcher m = p.matcher(sql);
        if (m.find()) {
            String dbName = m.group(1);
            databases.put(dbName, new Database(dbName));
            saveDatabase(dbName);
            return "数据库 '" + dbName + "' 创建成功并已保存";
        }
        return "创建数据库失败";
    }
    
    private String dropDatabase(String sql) {
        Pattern p = Pattern.compile("drop\\s+database\\s+(\\w+)", Pattern.CASE_INSENSITIVE);
        Matcher m = p.matcher(sql);
        if (m.find()) {
            String dbName = m.group(1);
            if (databases.remove(dbName) != null) {
                if (currentDatabase != null && currentDatabase.name.equals(dbName)) {
                    currentDatabase = null;
                }
                deleteDatabase(dbName);
                return "数据库 '" + dbName + "' 删除成功";
            }
            return "数据库 '" + dbName + "' 不存在";
        }
        return "删除数据库失败";
    }
    
    private String useDatabase(String sql) {
        Pattern p = Pattern.compile("use\\s+(\\w+)", Pattern.CASE_INSENSITIVE);
        Matcher m = p.matcher(sql);
        if (m.find()) {
            String dbName = m.group(1);
            if (databases.containsKey(dbName)) {
                currentDatabase = databases.get(dbName);
                return "切换到数据库 '" + dbName + "'";
            }
            return "数据库 '" + dbName + "' 不存在";
        }
        return "使用数据库失败";
    }
    
    private String createTable(String sql) {
        if (currentDatabase == null) {
            return "错误: 未选择数据库";
        }
        
        Pattern p = Pattern.compile("create\\s+table\\s+(\\w+)\\s*\\((.+)\\)", Pattern.CASE_INSENSITIVE | Pattern.DOTALL);
        Matcher m = p.matcher(sql);
        if (m.find()) {
            String tableName = m.group(1);
            String columnDef = m.group(2);
            
            List<String> columns = new ArrayList<>();
            String[] parts = columnDef.split(",");
            for (String part : parts) {
                part = part.trim();
                if (part.toLowerCase().startsWith("primary key")) {
                    continue;
                }
                String[] tokens = part.trim().split("\\s+");
                if (tokens.length >= 1) {
                    columns.add(tokens[0]);
                }
            }
            
            currentDatabase.createTable(tableName, columns);
            saveDatabase(currentDatabase.name);
            return "表 '" + tableName + "' 创建成功，包含 " + columns.size() + " 列";
        }
        return "创建表失败";
    }
    
    private String insertInto(String sql) {
        if (currentDatabase == null) {
            return "错误: 未选择数据库";
        }
        
        Pattern p = Pattern.compile("insert\\s+into\\s+(\\w+)\\s+values\\s*\\((.+)\\)", Pattern.CASE_INSENSITIVE | Pattern.DOTALL);
        Matcher m = p.matcher(sql);
        if (m.find()) {
            String tableName = m.group(1);
            String valueStr = m.group(2);
            
            List<String> values = parseValues(valueStr);
            currentDatabase.insertInto(tableName, values);
            saveDatabase(currentDatabase.name);
            return "向表 '" + tableName + "' 插入 1 行数据";
        }
        return "插入数据失败";
    }
    
    private String deleteFrom(String sql) {
        if (currentDatabase == null) {
            return "错误: 未选择数据库";
        }
        
        // 解析 DELETE FROM table WHERE condition
        Pattern p = Pattern.compile("delete\\s+from\\s+(\\w+)(?:\\s+where\\s+(.+))?", Pattern.CASE_INSENSITIVE | Pattern.DOTALL);
        Matcher m = p.matcher(sql);
        if (m.find()) {
            String tableName = m.group(1);
            String whereClause = m.group(2);
            
            int deletedCount = currentDatabase.deleteFrom(tableName, whereClause);
            saveDatabase(currentDatabase.name);
            return "从表 '" + tableName + "' 删除 " + deletedCount + " 行数据";
        }
        return "删除数据失败";
    }
    
    private List<String> parseValues(String valueStr) {
        List<String> values = new ArrayList<>();
        boolean inQuote = false;
        StringBuilder current = new StringBuilder();
        
        for (int i = 0; i < valueStr.length(); i++) {
            char c = valueStr.charAt(i);
            if (c == '\'') {
                inQuote = !inQuote;
            } else if (c == ',' && !inQuote) {
                values.add(current.toString().trim().replace("'", ""));
                current = new StringBuilder();
            } else {
                current.append(c);
            }
        }
        if (current.length() > 0) {
            values.add(current.toString().trim().replace("'", ""));
        }
        return values;
    }
    
    private String select(String sql) {
        if (currentDatabase == null) {
            return "错误: 未选择数据库";
        }
        
        try {
            SelectQuery query = parseSelect(sql);
            outputArea.append("  解析: 表=" + query.tables + ", WHERE=" + query.whereClause + "\n");
            List<Map<String, String>> result = currentDatabase.executeSelect(query);
            displayResult(result, query.columns);
            return "查询完成，返回 " + result.size() + " 行数据";
        } catch (Exception e) {
            e.printStackTrace();
            return "查询失败: " + e.getMessage();
        }
    }
    
    private SelectQuery parseSelect(String sql) {
        SelectQuery query = new SelectQuery();
        
        // 提取SELECT和FROM之间的列
        Pattern selectPattern = Pattern.compile("select\\s+(.+?)\\s+from\\s+(.+?)(?:\\s+where\\s+(.+))?$", 
            Pattern.CASE_INSENSITIVE | Pattern.DOTALL);
        Matcher m = selectPattern.matcher(sql.trim());
        
        if (m.find()) {
            String columnPart = m.group(1).trim();
            String tablePart = m.group(2).trim();
            String wherePart = m.group(3);
            
            // 解析列
            if (columnPart.equals("*")) {
                query.selectAll = true;
            } else {
                String[] cols = columnPart.split(",");
                for (String col : cols) {
                    query.columns.add(col.trim());
                }
            }
            
            // 解析表
            String[] tables = tablePart.split(",");
            for (String table : tables) {
                query.tables.add(table.trim());
            }
            
            // 解析WHERE条件
            if (wherePart != null && !wherePart.trim().isEmpty()) {
                query.whereClause = wherePart.trim();
            }
        }
        
        return query;
    }
    
    private void displayResult(List<Map<String, String>> result, List<String> columns) {
        tableModel.setRowCount(0);
        tableModel.setColumnCount(0);
        
        if (result.isEmpty()) {
            return;
        }
        
        // 设置列
        List<String> displayColumns = columns;
        if (displayColumns.isEmpty()) {
            displayColumns = new ArrayList<>(result.get(0).keySet());
        }
        
        for (String col : displayColumns) {
            tableModel.addColumn(col);
        }
        
        // 添加数据
        for (Map<String, String> row : result) {
            Object[] rowData = new Object[displayColumns.size()];
            for (int i = 0; i < displayColumns.size(); i++) {
                rowData[i] = row.get(displayColumns.get(i));
            }
            tableModel.addRow(rowData);
        }
    }
    
    // 数据库类
    static class Database implements Serializable {
        private static final long serialVersionUID = 1L;
        String name;
        Map<String, Table> tables = new HashMap<>();
        
        Database(String name) {
            this.name = name;
        }
        
        void createTable(String tableName, List<String> columns) {
            tables.put(tableName, new Table(tableName, columns));
        }
        
        void insertInto(String tableName, List<String> values) {
            if (tables.containsKey(tableName)) {
                tables.get(tableName).insert(values);
            }
        }
        
        int deleteFrom(String tableName, String whereClause) {
            if (!tables.containsKey(tableName)) {
                return 0;
            }
            
            Table table = tables.get(tableName);
            if (whereClause == null || whereClause.trim().isEmpty()) {
                // 删除所有行
                int count = table.rows.size();
                table.rows.clear();
                return count;
            }
            
            // 根据WHERE条件删除
            List<Map<String, String>> toDelete = new ArrayList<>();
            for (Map<String, String> row : table.rows) {
                if (evaluateWhere(row, whereClause.trim(), Arrays.asList(tableName))) {
                    toDelete.add(row);
                }
            }
            
            table.rows.removeAll(toDelete);
            return toDelete.size();
        }
        
        List<Map<String, String>> executeSelect(SelectQuery query) {
            if (query.tables.isEmpty()) {
                return new ArrayList<>();
            }
            
            // 获取第一个表的数据
            List<Map<String, String>> result = new ArrayList<>();
            Table firstTable = tables.get(query.tables.get(0));
            if (firstTable == null) {
                return result;
            }
            
            // 如果只有一个表
            if (query.tables.size() == 1) {
                for (Map<String, String> row : firstTable.rows) {
                    if (query.whereClause == null || evaluateWhere(row, query.whereClause, query.tables)) {
                        Map<String, String> newRow = new HashMap<>(row);
                        result.add(newRow);
                    }
                }
            } else {
                // 多表连接（笛卡尔积或JOIN）
                result = cartesianProduct(query.tables, 0, new LinkedHashMap<>(), query);
            }
            
            // 选择列
            if (!query.selectAll && !query.columns.isEmpty()) {
                List<Map<String, String>> filtered = new ArrayList<>();
                for (Map<String, String> row : result) {
                    Map<String, String> newRow = new LinkedHashMap<>();
                    for (String col : query.columns) {
                        newRow.put(col, row.get(col));
                    }
                    filtered.add(newRow);
                }
                return filtered;
            }
            
            return result;
        }
        
        private List<Map<String, String>> cartesianProduct(List<String> tableNames, int index, 
                Map<String, String> currentRow, SelectQuery query) {
            List<Map<String, String>> result = new ArrayList<>();
            
            if (index >= tableNames.size()) {
                // 所有表都处理完了，评估WHERE条件
                if (query.whereClause == null || evaluateWhere(currentRow, query.whereClause, tableNames)) {
                    result.add(new LinkedHashMap<>(currentRow));
                }
                return result;
            }
            
            String tableName = tableNames.get(index);
            Table table = tables.get(tableName);
            if (table == null) {
                return result;
            }
            
            // 对当前表的每一行
            for (Map<String, String> row : table.rows) {
                Map<String, String> newRow = new LinkedHashMap<>(currentRow);
                
                // 添加当前表的列（处理列名冲突）
                for (Map.Entry<String, String> entry : row.entrySet()) {
                    String key = entry.getKey();
                    String value = entry.getValue();
                    
                    // 如果列名已存在且值不同，使用表名.列名的格式
                    if (newRow.containsKey(key)) {
                        newRow.put(tableName + "." + key, value);
                    } else {
                        newRow.put(key, value);
                    }
                }
                
                // 递归处理下一个表
                result.addAll(cartesianProduct(tableNames, index + 1, newRow, query));
            }
            
            return result;
        }
        
        private boolean evaluateWhere(Map<String, String> row, String whereClause, List<String> tableNames) {
            // 分割AND条件 - 使用正则表达式来正确处理
            List<String> conditions = new ArrayList<>();
            String[] parts = whereClause.toLowerCase().split("\\s+and\\s+");
            
            // 重新定位原始字符串中的条件
            int pos = 0;
            for (String part : parts) {
                int idx = whereClause.toLowerCase().indexOf(part, pos);
                if (idx >= 0) {
                    int endIdx = idx + part.length();
                    // 找到下一个 "and" 的位置
                    int nextAnd = whereClause.toLowerCase().indexOf(" and ", endIdx);
                    if (nextAnd > 0) {
                        conditions.add(whereClause.substring(idx, nextAnd).trim());
                        pos = nextAnd + 5; // " and " 的长度
                    } else {
                        conditions.add(whereClause.substring(idx).trim());
                        break;
                    }
                }
            }
            
            if (conditions.isEmpty()) {
                conditions.add(whereClause);
            }
            
            for (String condition : conditions) {
                condition = condition.trim();
                if (!evaluateCondition(row, condition)) {
                    return false;
                }
            }
            return true;
        }
        
        private boolean evaluateCondition(Map<String, String> row, String condition) {
            // 处理等于
            if (condition.contains("=")) {
                int eqPos = condition.indexOf("=");
                String left = condition.substring(0, eqPos).trim();
                String right = condition.substring(eqPos + 1).trim();
                
                // 移除引号
                if (right.startsWith("'") && right.endsWith("'")) {
                    right = right.substring(1, right.length() - 1);
                }
                
                // 处理表名.列名格式
                String leftValue = getColumnValue(row, left);
                String rightValue = right;
                
                // 如果right也是列名，获取其值
                if (!condition.substring(eqPos + 1).trim().startsWith("'")) {
                    String rightFromRow = getColumnValue(row, right);
                    if (rightFromRow != null) {
                        rightValue = rightFromRow;
                    }
                }
                
                if (leftValue == null) {
                    return false;
                }
                if (rightValue == null) {
                    return false;
                }
                
                return leftValue.equals(rightValue);
            }
            
            // 处理大于
            if (condition.contains(">")) {
                int gtPos = condition.indexOf(">");
                String left = condition.substring(0, gtPos).trim();
                String right = condition.substring(gtPos + 1).trim();
                
                // 移除引号
                if (right.startsWith("'") && right.endsWith("'")) {
                    right = right.substring(1, right.length() - 1);
                }
                
                String leftValue = getColumnValue(row, left);
                if (leftValue == null) {
                    return false;
                }
                
                try {
                    double leftNum = Double.parseDouble(leftValue);
                    double rightNum = Double.parseDouble(right);
                    return leftNum > rightNum;
                } catch (NumberFormatException e) {
                    return leftValue.compareTo(right) > 0;
                }
            }
            
            return true;
        }
        
        private String getColumnValue(Map<String, String> row, String column) {
            // 如果是表名.列名格式
            if (column.contains(".")) {
                String[] parts = column.split("\\.", 2);
                String tableName = parts[0];
                String colName = parts[1];
                
                // 先尝试 表名.列名
                String value = row.get(tableName + "." + colName);
                if (value != null) {
                    return value;
                }
                
                // 再尝试只用列名
                return row.get(colName);
            }
            
            // 直接使用列名
            return row.get(column);
        }
    }
    
    // 表类
    static class Table implements Serializable {
        private static final long serialVersionUID = 1L;
        String name;
        List<String> columns;
        List<Map<String, String>> rows = new ArrayList<>();
        
        Table(String name, List<String> columns) {
            this.name = name;
            this.columns = columns;
        }
        
        void insert(List<String> values) {
            Map<String, String> row = new LinkedHashMap<>();
            for (int i = 0; i < columns.size() && i < values.size(); i++) {
                row.put(columns.get(i), values.get(i));
            }
            rows.add(row);
        }
    }
    
    // 查询对象
    static class SelectQuery {
        boolean selectAll = false;
        List<String> columns = new ArrayList<>();
        List<String> tables = new ArrayList<>();
        String whereClause = null;
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            SimpleDatabase db = new SimpleDatabase();
            db.setVisible(true);
        });
    }
}