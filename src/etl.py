from pyspark.sql import SparkSession
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def sanitize_column_names(df):
    """
    Replace invalid characters in DataFrame column names.
    """
    def clean_column_name(column_name):
        return re.sub(r'[ ,;{}()\n\t=]', '_', column_name)
    return df.toDF(*[clean_column_name(col) for col in df.columns])

def read_data(spark, file_path):
    """
    Load data from a CSV file.
    """
    return spark.read.format("csv").option("header", "true").load(file_path)

def write_data(df, output_path):
    """
    Write DataFrame to a Delta table with overwrite mode.
    """
    df.write.format("delta").mode("overwrite").save(output_path)

def main():
    logger.info("Begin processing ETL...")
    
    spark = None
    try:
        spark = SparkSession.builder \
            .appName("Delta Lake ETL Application") \
            .config("spark.jars.packages", "io.delta:delta-core_2.12:1.2.1") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .getOrCreate()
        logger.info("Spark session initialized successfully.")

        data_path = "/app/data/data.csv"
        output_path = "/app/output/delta_table"
        
        df = read_data(spark, data_path)
        df.show()

        df = sanitize_column_names(df)
        write_data(df, output_path)
        logger.info("Data written to Delta Lake successfully.")

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
    finally:
        if spark:
            spark.stop()
            logger.info("Spark session stopped.")

if __name__ == "__main__":
    main()
