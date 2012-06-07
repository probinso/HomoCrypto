#!/bin/sh
HADOOP_PATH=/data/hadoop/bin/bin/hadoop
HADOOP_STREAMING_PATH=/data/hadoop/bin/contrib/streaming/hadoop-*streaming*.jar
MAPPER_FILE=/home/hajya/HomoCrypto/program/bible_map.py
REDUCER_FILE=/home/hajya/HomoCrypto/program/bible_reduce.py
CIRCUITS_FILE=/home/hajya/HomoCrypto/program/circuits.py
HELPERS_FILE=/home/hajya/HomoCrypto/program/helpers.py
INPUT_LOCATION=/hdfs/user/hajya/jesus_fucking_christ.txt
OUTPUT_LOCATION=/tmp/bibleinbit2

$HADOOP_PATH jar $HADOOP_STREAMING_PATH \
			-D mapred.max.split.size=30KB \
			-D mapred.maps.tasks=152 \
			-D mapred.reduce.tasks=1 \
			-file $HELPERS_FILE \
			-file $CIRCUITS_FILE \
			-file $MAPPER_FILE -mapper $MAPPER_FILE \
			-file $REDUCER_FILE -reducer $REDUCER_FILE \
			-input $INPUT_LOCATION -output $OUTPUT_LOCATION
