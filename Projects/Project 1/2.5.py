import mysql.connector
import pandas as pd

from pandas import DataFrame

import scipy.stats as stats
import numpy as np


conn = mysql.connector.connect(user='root',password = '----',host='localhost',database='cse601-project1')



cursor = conn.cursor()

cursor.execute("select distinct  mf.exp,d.name from microarray_fact mf inner join probe pf on pf.pb_id = mf.pb_id inner join gene_fact gf on pf.UID = gf.UID inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where gf.go_id = '7154' and d.name = 'ALL' union select distinct  mf.exp,d.name from microarray_fact mf inner join probe pf on pf.pb_id = mf.pb_id inner join gene_fact gf on pf.UID = gf.UID inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where gf.go_id = '7154' and d.name = 'AML' union select distinct  mf.exp,d.name from microarray_fact mf inner join probe pf on pf.pb_id = mf.pb_id inner join gene_fact gf on pf.UID = gf.UID inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where gf.go_id = '7154' and d.name = 'colon tumor' union select distinct  mf.exp,d.name from microarray_fact mf inner join probe pf on pf.pb_id = mf.pb_id inner join gene_fact gf on pf.UID = gf.UID inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where gf.go_id = '7154' and d.name = 'breast tumor'")

#mycursor.execute("select  distinct mf.pb_id, mf.exp,gf.go_id,d.name from microarray_fact mf right join probe pf on pf.pb_id = mf.pb_id right join gene_fact gf on pf.UID = gf.UID right join clinical_fact cf on cf.s_id = mf.s_id right join disease d on d.ds_id = cf.ds_id where gf.go_id = '12502' and d.name='ALL'")
#mycursor2.execute("select  distinct mf.pb_id, mf.exp,gf.go_id,d.name from microarray_fact mf right join probe pf on pf.pb_id = mf.pb_id right join gene_fact gf on pf.UID = gf.UID right join clinical_fact cf on cf.s_id = mf.s_id right join disease d on d.ds_id = cf.ds_id where gf.go_id = '12502' and d.name!='ALL'")

data = cursor.fetchall()
print("printing data from sql")
print(data)

all = []
colon_tumor = []
aml = []
breast_tumor = []


for row in data:

    if(row[1]=='ALL'):
        all.append(row[0])

    elif(row[1]=='AML'):
        aml.append(row[0])

    elif(row[1]=='Colon tumor'):
        colon_tumor.append(row[0])

    elif(row[1]=='Breast tumor'):
        breast_tumor.append(row[0])

size = all.__len__() +aml.__len__()+colon_tumor.__len__()+breast_tumor.__len__()
print(size)

print("printing the disease patients")
print(all)
print(aml)
print(colon_tumor)
print(breast_tumor)

x = stats.f_oneway(all,aml,colon_tumor,breast_tumor)
print(x)








