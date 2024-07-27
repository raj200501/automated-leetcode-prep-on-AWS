# EMR Setup

1. Launch an EMR cluster with Spark.
2. SSH into the master node.
3. Submit the Spark job using the following command:
    ```
    spark-submit --deploy-mode cluster s3://YOUR_SCRIPT_LOCATION/spark_job.py
    ```
