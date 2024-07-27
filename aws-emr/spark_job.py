from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("LeetCodeDataProcessing") \
    .getOrCreate()

df = spark.read.json("s3://leetcode-prep-bucket/processed-problems/")
df.createOrReplaceTempView("problems")

result = spark.sql("""
    SELECT difficulty, COUNT(*) as count
    FROM problems
    GROUP BY difficulty
""")

result.write.mode("overwrite").json("s3://leetcode-prep-bucket/analysis-results/")
