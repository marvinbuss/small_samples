'''
NOTE:
    This sample can be used, in Spark or Databricks, if your csv file that is stored on Azure Data Lake Gen2 has multiple header rows, but you want to use only one of them.
    If this is the case, then you can use this code sample to drop the unwanted rows and let spark infer the schema.
    Here, the second and third row are dropped (see line 15). 
'''

# set values
STORAGE_ACCOUNT_NAME = "<your-storage-account-name>"
STORAGE_CONTAINER = "<your-storage-container>"
LOCAL_FILE_PATH = "<your-file-path>"
SCOPE_NAME = "<your-scope-name>"
KEY_NAME = "<key-name-for-your-storage-account-access-key>"

# set the credentials to access the azure data lake v2 storage resource
sc._jsc.hadoopConfiguration().set(
  "fs.azure.account.key." + STORAGE_ACCOUNT_NAME + ".dfs.core.windows.net",
  dbutils.secrets.get(scope = SCOPE_NAME, key = KEY_NAME))

# set the file path and load the raw data
FILE_PATH = "abfss://" + STORAGE_CONTAINER + "@" + STORAGE_ACCOUNT_NAME + ".dfs.core.windows.net/" + LOCAL_FILE_PATH
data = sc.textFile(FILE_PATH)

# save the lines that should be dropped
lines_to_filter = data.take(3)[1:]

# filter the lines
data_filtered = data.filter(lambda x: None if x in lines_to_filter else x)

# read the data as dataframe
# Alternative: df_new = data_filtered.toDF(schema=<your_schema>)
df_new = spark.read.option("header", "true").csv(data_filtered)

display(df_new)
