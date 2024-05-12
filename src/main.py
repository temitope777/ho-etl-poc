from pyspark.sql import SparkSession
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def sanitize_column_names(df):
    def clean_column_name(column_name):
        # Remove or replace invalid characters in column names
        return re.sub(r'[ ,;{}()\n\t=]', '_', column_name)
    
    return df.toDF(*[clean_column_name(col) for col in df.columns])

def main():
    logger.info("Starting the ETL process...")
    
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
        
        df = spark.read.format("csv").option("header", "true").load(data_path)
        df.show()

        # Sanitize column names
        df = sanitize_column_names(df)
        
        df.write.format("delta").mode("overwrite").save(output_path)
        logger.info("Data written to Delta Lake successfully.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        spark.stop()
        logger.info("Spark session stopped.")

if __name__ == "__main__":
    main()
