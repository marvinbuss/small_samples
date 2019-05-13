'''
NOTE:
    This sample can be used, in Spark or Databricks, if your csv file has multiple header rows, but you want to use only one of them.
    If this is the case, then you can use this code sample to drop the unwanted rows and let spark infer the schema.
    Here, the second and third row are dropped (see line 15). 
'''

# file path to your csv file
FILE_PATH = '<your-file-path>' # e.g. '/FileStore/tables/test.csv'

# read file as textfile
data = sc.textFile(FILE_PATH)

# save the lines that should be dropped
lines_to_filter = data.take(3)[1:]

# filter the lines
data_filtered = data.filter(lambda x: None if x in lines_to_filter else x)

# read the data as dataframe
# Alternative: df_new = data_filtered.toDF(schema=<your_schema>)
df_new = spark.read.option("header", "true").csv(data_filtered)
display(df_new)