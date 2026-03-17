#!/bin/bash
set -e

BASE=~/hadoop_experiment2
HDFS_IN=/user/darren/exp2/input
HDFS_OUT=/user/darren/exp2/output
HADOOP_HOME=/usr/local/hadoop
#启动DFS和YARN
$HADOOP_HOME/sbin/start-dfs.sh > /dev/null 2>&1
$HADOOP_HOME/sbin/start-yarn.sh > /dev/null 2>&1
echo "=== 实验二：随机数排序 MapReduce 程序运行开始 ==="

mkdir -p $BASE
mkdir -p $BASE/classes

# 1. 生成输入文件
echo "=== 生成随机输入文件 ==="
for f in file1.txt file2.txt; do
    shuf -i 1-100 -n 10 > $BASE/$f
done

# 2. 编译 Java
echo "=== 编译 Java 程序 ==="
javac -classpath "$HADOOP_HOME/share/hadoop/common/*:$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/yarn/*" \
      -d $BASE/classes \
      $BASE/DescSortClean.java

# 3. 打包 jar
echo "=== 打包 JAR ==="
jar -cvf $BASE/DescSortClean.jar -C $BASE/classes .

# 4. 退出 HDFS Safe Mode（防止连接被拒绝）
echo "=== 确保 HDFS 可写 ==="
hdfs dfsadmin -safemode leave

# 4. 清理 HDFS 目录
echo "=== 准备 HDFS 目录 ==="
hdfs dfs -rm -r -f $HDFS_IN $HDFS_OUT
hdfs dfs -mkdir -p $HDFS_IN

# 5. 上传两个文件到 HDFS
echo "=== 上传输入文件到 HDFS ==="
hdfs dfs -put $BASE/file1.txt $BASE/file2.txt $HDFS_IN/

# 6. 运行 MapReduce
echo "=== 运行 MapReduce 任务 ==="
hadoop jar $BASE/DescSortClean.jar DescSortClean $HDFS_IN $HDFS_OUT

# 7. 输出最终结果
echo "=== 最终排序结果 ==="
hdfs dfs -cat $HDFS_OUT/part-r-00000

echo "=== 实验二完成 ==="
