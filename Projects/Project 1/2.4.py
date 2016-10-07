import pymysql as mysql
from scipy.stats import ttest_ind

conn = mysql.connect(user='root', password='-----', host='localhost', database='cse601-project1')
conn2 = mysql.connect(user='root', password='----', host='localhost', database='cse601-project1')

conn_data1 = conn.cursor()
conn_data2 = conn2.cursor()

conn_data1.execute(
    "select  distinct mf.pb_id, mf.exp,gf.go_id,d.name "
    "from microarray_fact mf "
    "inner join probe pf on pf.pb_id = mf.pb_id "
    "inner join gene_fact gf on pf.UID = gf.UID "
    "inner join clinical_fact cf on cf.s_id = mf.s_id "
    "inner join disease d on d.ds_id = cf.ds_id "
    "where gf.go_id = '12502' and d.name='ALL'")
conn_data2.execute(
    "select  distinct mf.pb_id, mf.exp,gf.go_id,d.name "
    "from microarray_fact mf "
    "inner join probe pf on pf.pb_id = mf.pb_id "
    "inner join gene_fact gf on pf.UID = gf.UID "
    "inner join clinical_fact cf on cf.s_id = mf.s_id "
    "inner join disease d on d.ds_id = cf.ds_id "
    "where gf.go_id = '12502' and d.name!='ALL'")
data1 = conn_data1.fetchall()
data2 = conn_data2.fetchall()

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

x = ttest_ind(all, not_all, equal_var=True)
print(x)
