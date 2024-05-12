from pyspark.sql import SparkSession
from behave import given, when, then
import re
import os

def get_spark_session():
    spark = SparkSession.builder \
        .appName("Delta Lake BDD Testing") \
        .master("local") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:1.2.1") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    return spark

def sanitize_column_names(df):
    def clean_column_name(column_name):
        return re.sub(r'[ ,;{}()\n\t=]', '_', column_name)

    return df.toDF(*[clean_column_name(col) for col in df.columns])

@given('a CSV file with data')
def step_impl_given(context):
    context.spark = get_spark_session()
    context.data_path = "/app/data/data.csv"
    assert os.path.exists(context.data_path), "Data file does not exist"

@when('the ETL process is executed')
def step_impl_when(context):
    df = context.spark.read.format("csv").option("header", "true").load(context.data_path)
    # Sanitize column names before writing to Delta Lake
    df = sanitize_column_names(df)
    context.output_path = "/app/output/delta_table"
    df.write.format("delta").option("mergeSchema", "true").mode("overwrite").save(context.output_path)

@then('the output should be stored in Delta Lake format without errors')
def step_impl_then(context):
    df = context.spark.read.format("delta").load(context.output_path)
    assert df.count() > 0, "No data found in Delta table"
    context.spark.stop()
