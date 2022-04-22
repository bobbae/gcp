# -*- coding: utf-8 -*-
"""Basic BigQuery demo
"""

# If running from cloud-shell, DEVSHELL_PROJECT_ID environment variable may contain project ID.
# import os
# project_id = os.getenv("DEVSHELL_PROJECT_ID")

# Otherwise, set project_id manually
# project_id = 'XXXyourprojectID'

#from google.colab import auth
#auth.authenticate_user()
#print('Authenticated')

project_id = 'project-u-5'

"""### BigQuery and dataframe"""

from google.cloud import bigquery

client = bigquery.Client(project=project_id)

sample_count = 2000
row_count = client.query('''
  SELECT 
    COUNT(*) as total
  FROM `bigquery-public-data.samples.gsod`''').to_dataframe().total[0]

print('row_count',row_count)

#df = client.query('''
#  SELECT
#    *
#  FROM
#    `bigquery-public-data.samples.gsod`
#  WHERE RAND() < %d/%d
#''' % (sample_count, row_count)).to_dataframe()
#
#print('Full dataset has %d rows' % row_count)
#
#"""### Describe the sampled data"""
#
#df.describe()
#
#"""### View the first 10 rows"""
#
#df.head(10)
#
## 10 highest total_precipitation samples
#df.sort_values('total_precipitation', ascending=False).head(10)[['station_number', 'year', 'month', 'day', 'total_precipitation']]
#
#"""### Use BigQuery through pandas-gbq
#
#The `pandas-gbq` library is a community led project by the pandas community. It covers basic functionality, such as writing a DataFrame to BigQuery and running a query, but as a third-party library it may not handle all BigQuery features or use cases.
#
#[Pandas GBQ Documentation](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_gbq.html)
#"""
#
#import pandas as pd
#
#sample_count = 2000
#df = pd.io.gbq.read_gbq('''
#  SELECT name, SUM(number) as count
#  FROM `bigquery-public-data.usa_names.usa_1910_2013`
#  WHERE state = 'TX'
#  GROUP BY name
#  ORDER BY count DESC
#  LIMIT 100
#''', project_id=project_id, dialect='standard')
#
#df.head()
#
#"""### Syntax highlighting
#`google.colab.syntax` can be used to add syntax highlighting to any Python string literals which are used in a query later.
#"""
#
#from google.colab import syntax
#query = syntax.sql('''
#SELECT
#  COUNT(*) as total_rows
#FROM
#  `bigquery-public-data.samples.gsod`
#''')
#
#pd.io.gbq.read_gbq(query, project_id=project_id, dialect='standard')
#
