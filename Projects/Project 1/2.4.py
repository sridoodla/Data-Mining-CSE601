import mysql.connector
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

conn = mysql.connector.connect(user='root',password = '-----',host='localhost',database='cse601-project1')
conn2 = mysql.connector.connect(user='root',password = '----',host='localhost',database='cse601-project1')


mycursor = conn.cursor()
mycursor2 = conn2.cursor()

#mycursor.execute("select distinct  mf.exp,d.name from microarray_fact mf inner join probe pf on pf.pb_id = mf.pb_id inner join gene_fact gf on pf.UID = gf.UID inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where gf.go_id = '7154' and d.name = 'ALL' union select distinct  mf.exp,d.name from microarray_fact mf inner join probe pf on pf.pb_id = mf.pb_id inner join gene_fact gf on pf.UID = gf.UID inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where gf.go_id = '7154' and d.name = 'AML' union select distinct  mf.exp,d.name from microarray_fact mf inner join probe pf on pf.pb_id = mf.pb_id inner join gene_fact gf on pf.UID = gf.UID inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where gf.go_id = '7154' and d.name = 'colon tumor' union select distinct  mf.exp,d.name from microarray_fact mf inner join probe pf on pf.pb_id = mf.pb_id inner join gene_fact gf on pf.UID = gf.UID inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where gf.go_id = '7154' and d.name = 'breast tumor'")

mycursor.execute("select  distinct mf.pb_id, mf.exp,gf.go_id,d.name from microarray_fact mf inner join probe pf on pf.pb_id = mf.pb_id inner join gene_fact gf on pf.UID = gf.UID inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where gf.go_id = '12502' and d.name='ALL'")
mycursor2.execute("select  distinct mf.pb_id, mf.exp,gf.go_id,d.name from microarray_fact mf inner join probe pf on pf.pb_id = mf.pb_id inner join gene_fact gf on pf.UID = gf.UID inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where gf.go_id = '12502' and d.name!='ALL'")
data1 = mycursor.fetchall()
data2 = mycursor2.fetchall()
print("printing data from sql")
print(data1)
print(data2)

all = []
not_all = []


for row in data1:
    all.append(row[1])

for row in data2:
    not_all.append(row[1])

size1 = all.__len__()
size2 = not_all.__len__()
print(size1)
print(size2)

print("printing the disease patients")
print(all)
print(not_all)

x = ttest_ind(all,not_all,equal_var = True)
print(x)








