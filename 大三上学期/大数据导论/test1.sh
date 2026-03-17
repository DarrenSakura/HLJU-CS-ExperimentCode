#!/bin/bash
USER_NAME=darren
FILE_LOCATION=/home/$USER_NAME/hadoop_experiment1/demo.txt
HDFS_DIR=/user/$USER_NAME/demo
HADOOP_HOME=/usr/local/hadoop
#启动DFS和YARN
$HADOOP_HOME/sbin/start-dfs.sh > /dev/null 2>&1
$HADOOP_HOME/sbin/start-yarn.sh > /dev/null 2>&1
#等待NameNode启动
sleep 5
#上传文件
hdfs dfs -put -f $FILE_LOCATION $HDFS_DIR/ > /dev/null 2>&1
#显示HDFS目录
echo  "HDFS目录内容:"
hdfs dfs -ls $HDFS_DIR 2>/dev/null | awk 'NF==8{print $8}'
#显示文件内容
echo "文件内容:"
hdfs dfs -cat $HDFS_DIR/$(basename $FILE_LOCATION) 2>/dev/null
