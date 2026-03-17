#!/bin/bash
set -e
BASE=~/hadoop_experiment3
HDFS_IN=/user/darren/exp3/input
HDFS_OUT1=/user/darren/exp3/output1
HDFS_OUT2=/user/darren/exp3/output2
HADOOP_HOME=/usr/local/hadoop
#启动DFS和YARN
$HADOOP_HOME/sbin/start-dfs.sh > /dev/null 2>&1
$HADOOP_HOME/sbin/start-yarn.sh > /dev/null 2>&1
echo "=== 实验三：词频统计 + 降序 Top10 ==="
mkdir -p $BASE/classes
# 退出 SafeMode
hdfs dfsadmin -safemode leave 2>/dev/null || true
# 清理 HDFS 目录
echo "=== 准备 HDFS 目录 ==="
hdfs dfs -rm -r -f $HDFS_IN $HDFS_OUT1 $HDFS_OUT2
hdfs dfs -mkdir -p $HDFS_IN
# 上传输入文件
echo "=== 上传 document.txt 到 HDFS ==="
hdfs dfs -put $BASE/document.txt $HDFS_IN/
# 编译
echo "=== 编译 Java 文件 ==="
javac -classpath "$HADOOP_HOME/share/hadoop/common/*:$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/yarn/*" \
      -d $BASE/classes \
      $BASE/WordCount.java \
      $BASE/SortByCount.java
# 打包
echo "=== 打包 JAR ==="
jar -cvf $BASE/Exp3.jar -C $BASE/classes .
# 第一次 MR：词频统计
echo "=== 运行 WordCount ==="
hadoop jar $BASE/Exp3.jar WordCount $HDFS_IN $HDFS_OUT1
# 第二次 MR：排序 Top 10
echo "=== 运行 SortByCount ==="
hadoop jar $BASE/Exp3.jar SortByCount $HDFS_OUT1 $HDFS_OUT2
# 结果
echo "=== 最终 Top 10 高频词 ==="
hdfs dfs -cat $HDFS_OUT2/part-r-00000
echo "=== 实验三完成 ==="
