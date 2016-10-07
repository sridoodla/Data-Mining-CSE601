import pymysql as mysql
import scipy.stats as stats

conn = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')

cursor = conn.cursor()

cursor.execute(
    "select distinct  mf.exp,d.name "
    "from microarray_fact mf "
    "inner join probe pf on pf.pb_id = mf.pb_id "
    "inner join gene_fact gf on pf.UID = gf.UID "
    "inner join clinical_fact cf on cf.s_id = mf.s_id "
    "inner join disease d on d.ds_id = cf.ds_id "
    "where gf.go_id = '7154' "
    "and d.name = 'ALL' "
    "union "
    "select distinct  mf.exp,d.name "
    "from microarray_fact mf "
    "inner join probe pf on pf.pb_id = mf.pb_id "
    "inner join gene_fact gf on pf.UID = gf.UID "
    "inner join clinical_fact cf on cf.s_id = mf.s_id "
    "inner join disease d on d.ds_id = cf.ds_id "
    "where gf.go_id = '7154' and d.name = 'AML' "
    "union "
    "select distinct  mf.exp,d.name "
    "from microarray_fact mf "
    "inner join probe pf on pf.pb_id = mf.pb_id "
    "inner join gene_fact gf on pf.UID = gf.UID "
    "inner join clinical_fact cf on cf.s_id = mf.s_id "
    "inner join disease d on d.ds_id = cf.ds_id "
    "where gf.go_id = '7154' and d.name = 'colon tumor' "
    "union "
    "select distinct  mf.exp,d.name "
    "from microarray_fact mf "
    "inner join probe pf on pf.pb_id = mf.pb_id "
    "inner join gene_fact gf on pf.UID = gf.UID "
    "inner join clinical_fact cf on cf.s_id = mf.s_id "
    "inner join disease d on d.ds_id = cf.ds_id "
    "where gf.go_id = '7154' and d.name = 'breast tumor'")

data = cursor.fetchall()
all = []
colon_tumor = []
aml = []
breast_tumor = []

for row in data:

    if (row[1] == 'ALL'):
        all.append(row[0])

    elif (row[1] == 'AML'):
        aml.append(row[0])

    elif (row[1] == 'Colon tumor'):
        colon_tumor.append(row[0])

    elif (row[1] == 'Breast tumor'):
        breast_tumor.append(row[0])

size = all.__len__() + aml.__len__() + colon_tumor.__len__() + breast_tumor.__len__()
print(size)

print("printing the disease patients")
print(all)
print(aml)
print(colon_tumor)
print(breast_tumor)

x = stats.f_oneway(all, aml, colon_tumor, breast_tumor)
print(x)
