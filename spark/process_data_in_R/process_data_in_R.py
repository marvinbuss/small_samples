# Databricks notebook source
# MAGIC %md
# MAGIC # 0. Read Parameters from Azure Data Factory
# MAGIC 
# MAGIC https://docs.microsoft.com/en-us/azure/data-factory/transform-data-using-databricks-notebook#create-a-pipeline

# COMMAND ----------

# Creating widgets for leveraging parameters, and printing the parameters
dbutils.widgets.text("input", "","")
dbutils.widgets.get("input")
parameter = getArgument("input")
print (parameter)

# COMMAND ----------

# MAGIC %md
# MAGIC # 1. Access to Data Lake Gen 2

# COMMAND ----------

# set parameters
STORAGE_ACCOUNT_NAME = "<your-storageaccount-name>"
STORAGE_CONTAINER = "<your-storageaccount-container-name>"
LOCAL_FILE_PATH = "<your-local-file-path>"
SCOPE_NAME = "<your-db-secrets-scope-name>"
KEY_NAME = "<your-db-secrets-key-name>"

# COMMAND ----------

# set the credentials to access the azure data lake v2 storage resource
spark.conf.set(
  "fs.azure.account.key." + STORAGE_ACCOUNT_NAME + ".dfs.core.windows.net",
  dbutils.secrets.get(scope = SCOPE_NAME, key = KEY_NAME)
)

# COMMAND ----------

# list files in filepath
FOLDER_PATH = "abfss://" + STORAGE_CONTAINER + "@" + STORAGE_ACCOUNT_NAME + ".dfs.core.windows.net/"
file_list = dbutils.fs.ls(FOLDER_PATH)

# COMMAND ----------

data = spark.read.csv(file_list[0].path)
display(data)

# COMMAND ----------

# Register table so it is accessible via R Context
data.createOrReplaceTempView("data")

# COMMAND ----------

# MAGIC %md
# MAGIC # 2. Access Data in SQL

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM data

# COMMAND ----------

# MAGIC %md
# MAGIC # 3. Access Data in SparkR

# COMMAND ----------

# MAGIC %r
# MAGIC library(SparkR)
# MAGIC data <- sql("SELECT * FROM data")
# MAGIC display(data)

# COMMAND ----------

# MAGIC %md
# MAGIC # 4. Convert Data to R data.frame

# COMMAND ----------

# MAGIC %r
# MAGIC # save data in R data.frame
# MAGIC r_data <- collect(data)

# COMMAND ----------

# MAGIC %md
# MAGIC # 5. Execute R Script 

# COMMAND ----------

# MAGIC %r
# MAGIC #####################################
# MAGIC # TODO
# MAGIC #####################################
# MAGIC 
# MAGIC # insert script here
# MAGIC 
# MAGIC # Remove this line. This is just a placeholder to demonstrate the next steps
# MAGIC output <- data
# MAGIC 
# MAGIC #####################################
# MAGIC # TODO
# MAGIC #####################################

# COMMAND ----------

# MAGIC %md
# MAGIC # 6. Pass Data to PySpark

# COMMAND ----------

# MAGIC %r
# MAGIC # Register table so it is accessible via Python Context
# MAGIC createOrReplaceTempView(output, "output")

# COMMAND ----------

# MAGIC %md
# MAGIC # 7. Access Data in PySpark

# COMMAND ----------

output = sql("SELECT * FROM output")
display(output)

# COMMAND ----------

# MAGIC %md
# MAGIC # 8. Save Output on Data Lake Gen 2

# COMMAND ----------

import os

OUTPUT_PATH = os.path.join(FOLDER_PATH, "output")
output.repartition(1).write.csv(OUTPUT_PATH, header=True)
