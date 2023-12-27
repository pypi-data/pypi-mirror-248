from pyspark.sql.functions import datediff

def calculate_age(df):
    df = df.withColumn('Opportunity_Age1', datediff('Close_Date', 'Created_Date'))
    return df
