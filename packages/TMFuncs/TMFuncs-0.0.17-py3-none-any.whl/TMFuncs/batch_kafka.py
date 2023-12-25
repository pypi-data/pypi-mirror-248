"""
Batch（批量） Kafka的处理、解析相关功能
"""


# 批量读取。根据需求，按照指定的消息时间戳的范围，一般默认是最近2日，防止kafka消息推送有延迟的情况
def read_kafka(spark_ob, kafka_servers, kafka_topics, unique_label,
               start_offsets_by_timestamp, end_offsets_by_timestamp):
    return spark_ob \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_servers) \
        .option("kafka.group.id", unique_label) \
        .option("kafka.session.timeout.ms", 30000) \
        .option("subscribe", kafka_topics) \
        .option("startingTimestamp", start_offsets_by_timestamp) \
        .option("endingTimestamp", end_offsets_by_timestamp) \
        .load()


# 批量写库
def write_deltaLake(events, file_format, db_name, table_name, blob_path, partition_cols, max_file_size, unique_label,
                    mode='append'):
    events.write \
        .format(file_format) \
        .mode("append") \
        .option("checkpointLocation", f"{blob_path}/{db_name}/{table_name}/{unique_label}/_checkpoints/") \
        .option("mergeSchema", 'true') \
        .option("delta.targetFileSize", max_file_size) \
        .option("path", f'{blob_path}/{db_name}/{table_name}') \
        .saveAsTable(f'{db_name}.{table_name}', partitionBy=partition_cols, mode=mode)