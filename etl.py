from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum

# Create a SparkSession
spark = SparkSession.builder \
    .appName("ETLPipeline") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.0.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Read data from CSV file
data_df = spark.read.csv("/data/data.csv", header=True, inferSchema=True)

# Apply transformation: calculate total order amount
transformed_df = data_df.withColumn("TotalAmount", col("Quantity") * col("Price"))

# Write the transformed data to a Delta Table
delta_table_path = "/delta/orders"
transformed_df.write.format("delta").mode("overwrite").save(delta_table_path)

# Stop the SparkSession
spark.stop()