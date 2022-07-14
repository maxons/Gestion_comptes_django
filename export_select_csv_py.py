import pymysql
import pandas as pd
import subprocess

connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='password',
                             db='app_gestion_django',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


with connection.cursor() as cursor:
    # Read a single record
    sql = "SELECT * FROM operation"
    cursor.execute(sql)

data = cursor.fetchall()
df = pd.DataFrame(data)
df.to_csv("/Users/maxons/Documents/django_projects/Gestion_comptes_django/test_csv_pd.csv")

connection.close()

subprocess.run("Rscript analyze_data.R", shell=True)
