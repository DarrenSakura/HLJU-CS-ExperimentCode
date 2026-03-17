#!/bin/bash
HADOOP_HOME=/usr/local/hadoop
#启动DFS和YARN
$HADOOP_HOME/sbin/start-dfs.sh > /dev/null 2>&1
$HADOOP_HOME/sbin/start-yarn.sh > /dev/null 2>&1
cd hadoop_experiment4
echo "电影关联度分析 MapReduce 任务"
# 设置 Hadoop 环境变量
export HADOOP_CLASSPATH=$(hadoop classpath)
hdfs dfsadmin -safemode leave 2>/dev/null || true
# ====================================
# 第0步：编译所有Java文件
# ====================================
echo "编译所有Java文件"
javac -classpath $HADOOP_CLASSPATH MovieCount.java
if [ $? -ne 0 ]; then
    echo "错误: MovieCount.java 编译失败"
    exit 1
fi
javac -classpath $HADOOP_CLASSPATH UserPairs.java
if [ $? -ne 0 ]; then
    echo "错误: UserPairs.java 编译失败"
    exit 1
fi
javac -classpath $HADOOP_CLASSPATH PairAggregate.java
if [ $? -ne 0 ]; then
    echo "错误: PairAggregate.java 编译失败"
    exit 1
fi
javac -classpath $HADOOP_CLASSPATH Association.java
if [ $? -ne 0 ]; then
    echo "错误: Association.java 编译失败"
    exit 1
fi
echo "所有Java文件编译成功"
# 打包成jar文件
echo "打包jar文件"
jar -cvf MovieCount.jar MovieCount*.class > /dev/null 2>&1
jar -cvf UserPairs.jar UserPairs*.class > /dev/null 2>&1
jar -cvf PairAggregate.jar PairAggregate*.class > /dev/null 2>&1
jar -cvf Association.jar Association*.class > /dev/null 2>&1
echo "所有jar文件打包完成"
# ====================================
# 第1步：准备输入数据
# ====================================
echo "准备输入数据"
# 检查ratings.txt是否存在
if [ ! -f "ratings.txt" ]; then
    echo "错误: ratings.txt 文件不存在"
    exit 1
fi
# 创建HDFS输入目录
hadoop fs -mkdir -p /input > /dev/null 2>&1
# 删除旧的ratings.txt（如果存在）
hadoop fs -rm /input/ratings.txt > /dev/null 2>&1
# 上传ratings.txt到HDFS
hadoop fs -put ratings.txt /input/
if [ $? -ne 0 ]; then
    echo "错误: 上传ratings.txt失败"
    exit 1
fi
echo "数据上传成功"
hadoop fs -ls /input/ratings.txt
# ====================================
# 第2步：运行 MovieCount
# ====================================
echo "运行 MovieCount (统计每个电影的评分次数)"
hadoop fs -rm -r /output/movie_counts > /dev/null 2>&1
hadoop jar MovieCount.jar MovieCount /input/ratings.txt /output/movie_counts
if [ $? -ne 0 ]; then
    echo "错误: MovieCount 任务失败"
    exit 1
fi
echo "MovieCount 完成，输出结果:"
hadoop fs -cat /output/movie_counts/part-r-00000
# ====================================
# 第3步：运行 UserPairs
# ====================================
echo "运行 UserPairs (生成用户观看的电影对)..."
hadoop fs -rm -r /output/user_pairs > /dev/null 2>&1
hadoop jar UserPairs.jar UserPairs /input/ratings.txt /output/user_pairs
if [ $? -ne 0 ]; then
    echo "错误: UserPairs 任务失败"
    exit 1
fi
echo "UserPairs 完成，输出结果:"
hadoop fs -cat /output/user_pairs/part-r-00000
# ====================================
# 第4步：运行 PairAggregate
# ====================================
echo "运行 PairAggregate (聚合电影对)"
hadoop fs -rm -r /output/pair_aggregate > /dev/null 2>&1
hadoop jar PairAggregate.jar PairAggregate /output/user_pairs /output/pair_aggregate
if [ $? -ne 0 ]; then
    echo "错误: PairAggregate 任务失败"
    exit 1
fi
echo "✓ PairAggregate 完成，输出结果:"
hadoop fs -cat /output/pair_aggregate/part-r-00000
# ====================================
# 第5步：运行 Association
# ====================================
echo "运行 Association (计算Jaccard相似度)"
hadoop fs -rm -r /output/association > /dev/null 2>&1
hadoop jar Association.jar Association /output/pair_aggregate /output/association
if [ $? -ne 0 ]; then
    echo "错误: Association 任务失败"
    exit 1
fi
echo "Association 完成"
# ====================================
# 最终结果
# ====================================
echo "最终结果"
hadoop fs -cat /output/association/part-m-00000
echo "实验四完成"
