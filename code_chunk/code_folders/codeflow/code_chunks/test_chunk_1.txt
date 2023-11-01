import pandas as pd
import numpy as np
from datetime import date
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("ETLExample").getOrCreate()

csv_file_path = "C:\\Users\\NITINS\\OneDrive - Capgemini\\CAPGEMINI\\PROJECT\\GEN AI\\FE_Deck\\cardscdm_2201.csv"

source_data = spark.read.csv(csv_file_path, header=True, inferSchema=True)

sorted_data = source_data.orderBy("AMRL_ACCEPT_DECLINE_IND")

filtered_data = sorted_data.filter(col("AMRL_NBR_OF_ASSOCS") >= 2)

filtered_data.createOrReplaceTempView("temp_table")

check_1 = """
    SELECT
        ORG,TYPE,AMRL_NBR_OF_ASSOCS,AMRL_STATUS,AMRL_LAST_MAINT_OPER,AMRL_ACCEPT_DECLINE_IND,AMRL_DECISION_DATE,AMRL_EDIT_OPER
    FROM
        temp_table
    WHERE
        AMRL_ACCEPT_DECLINE_IND == 'A'
"""

query_data_1 = spark.sql(check_1)


check_2 = """
    SELECT
        A,B,C,D
    FROM
        sample_table
    WHERE
        AMRL_ACCEPT_DECLINE == 30
"""

query_data_2 = spark.sql(check_2)


check_3 = """
	SELECT M1.PAPER, T.TITLE FROM MATCH M1, MATCH M2, TITLES T WHERE M1.PAPER = M2.PAPER AND M1.PAPER = T.PAPER AND M1.CODE = 601 AND M2.CODE = 602; 
"""


result_df_1 = query_data_1.toPandas()
result_df_2 = query_data_2.toPandas()
result_df_3 = query_data_3.toPandas()

print(result_df_1)
print(result_df_2)

# Save the results to Excel or another target
result_df_1.to_excel(target_file_path_1, index=False)
result_df_2.to_excel(target_file_path_2, index=False)
result_df_3.to_excel(target_file_path_3, index=False)

