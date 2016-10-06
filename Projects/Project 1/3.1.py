import mysql.connector
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

conn = mysql.connector.connect(user='root',password = '-----',host='localhost',database='cse601-project1')
conn2 = mysql.connector.connect(user='root',password = '-----',host='localhost',database='cse601-project1')


mycursor = conn.cursor()
mycursor2 = conn2.cursor()

disease = 'ALL'
#disease = 'AML'
#disease = 'Colon tumor'
#disease = 'Breast tumor'
#disease = 'Giloblastome'
#disease = 'Flu'

#mycursor.execute("select distinct  mf.exp,d.name from microarray_fact mf inner join probe pf on pf.pb_id = mf.pb_id inner join gene_fact gf on pf.UID = gf.UID inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where gf.go_id = '7154' and d.name = 'ALL' union select distinct  mf.exp,d.name from microarray_fact mf inner join probe pf on pf.pb_id = mf.pb_id inner join gene_fact gf on pf.UID = gf.UID inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where gf.go_id = '7154' and d.name = 'AML' union select distinct  mf.exp,d.name from microarray_fact mf inner join probe pf on pf.pb_id = mf.pb_id inner join gene_fact gf on pf.UID = gf.UID inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where gf.go_id = '7154' and d.name = 'colon tumor' union select distinct  mf.exp,d.name from microarray_fact mf inner join probe pf on pf.pb_id = mf.pb_id inner join gene_fact gf on pf.UID = gf.UID inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where gf.go_id = '7154' and d.name = 'breast tumor'")
print(disease)
if disease == 'ALL':
    mycursor.execute("select distinct gf.uid,mf.exp,d.name from gene_fact gf inner join probe p on p.UID = gf.UID inner join microarray_fact mf on mf.pb_id = p.pb_id inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where d.name = 'ALL'")
    mycursor2.execute("select distinct gf.uid,mf.exp,d.name from gene_fact gf inner join probe p on p.UID = gf.UID inner join microarray_fact mf on mf.pb_id = p.pb_id inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where d.name != 'ALL'")

elif disease == 'AML':
    mycursor.execute("select distinct gf.uid,mf.exp,d.name from gene_fact gf inner join probe p on p.UID = gf.UID inner join microarray_fact mf on mf.pb_id = p.pb_id inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where d.name = 'AML'")
    mycursor2.execute("select distinct gf.uid,mf.exp,d.name from gene_fact gf inner join probe p on p.UID = gf.UID inner join microarray_fact mf on mf.pb_id = p.pb_id inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where d.name != 'AML'")

elif disease == 'Colon tumor':
    mycursor.execute("select distinct gf.uid,mf.exp,d.name from gene_fact gf inner join probe p on p.UID = gf.UID inner join microarray_fact mf on mf.pb_id = p.pb_id inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where d.name = 'Colon tumor'")
    mycursor2.execute("select distinct gf.uid,mf.exp,d.name from gene_fact gf inner join probe p on p.UID = gf.UID inner join microarray_fact mf on mf.pb_id = p.pb_id inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where d.name != 'Colon tumor'")

elif disease == 'Breast tumor':
    mycursor.execute("select distinct gf.uid,mf.exp,d.name from gene_fact gf inner join probe p on p.UID = gf.UID inner join microarray_fact mf on mf.pb_id = p.pb_id inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where d.name = 'Breast tumor'")
    mycursor2.execute("select distinct gf.uid,mf.exp,d.name from gene_fact gf inner join probe p on p.UID = gf.UID inner join microarray_fact mf on mf.pb_id = p.pb_id inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where d.name != 'Breast tumor'")

elif disease == 'Giloblastome':
    mycursor.execute("select distinct gf.uid,mf.exp,d.name from gene_fact gf inner join probe p on p.UID = gf.UID inner join microarray_fact mf on mf.pb_id = p.pb_id inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where d.name = 'Giloblastome'")
    mycursor2.execute("select distinct gf.uid,mf.exp,d.name from gene_fact gf inner join probe p on p.UID = gf.UID inner join microarray_fact mf on mf.pb_id = p.pb_id inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where d.name != 'Giloblastome'")

elif disease == 'Flu':
    mycursor.execute("select distinct gf.uid,mf.exp,d.name from gene_fact gf inner join probe p on p.UID = gf.UID inner join microarray_fact mf on mf.pb_id = p.pb_id inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where d.name = 'Flu'")
    mycursor2.execute("select distinct gf.uid,mf.exp,d.name from gene_fact gf inner join probe p on p.UID = gf.UID inner join microarray_fact mf on mf.pb_id = p.pb_id inner join clinical_fact cf on cf.s_id = mf.s_id inner join disease d on d.ds_id = cf.ds_id where d.name != 'Flu'")


data1 = mycursor.fetchall()
data2 = mycursor2.fetchall()
print("printing data from sql")


l1 = []
l2 = []

d1 = dict()
d2 = dict()

for row in data1:
    l1.append(row[0])
    uid1 = row[0]
    exp1 = row[1]

    d1.setdefault(uid1, []).append(exp1)

for row in data2:
    l2.append(row[0])
    uid2 = row[0]
    exp2 = row[1]

    d2.setdefault(uid2, []).append(exp2)


print(l1.__len__())
print(l2.__len__())

print(len(d1))
print(len(d2))

print(d1)
print(d2)

if_gene = []
for key in d1:
    x = d1[key]
    y = d2[key]
    z = ttest_ind(x,y,equal_var = True)
    if(z[1] <0.01):
        if_gene.append(key)
        print(z)

print("Informatice genes")
print(if_gene)









