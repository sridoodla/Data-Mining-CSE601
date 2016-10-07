import pymysql as mysql
from scipy.stats import ttest_ind


def two_4(go_id, disease_name):
    conn1 = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')
    conn2 = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')

    conn_data1 = conn1.cursor()
    conn_data2 = conn2.cursor()

    conn_data1.execute(
        "select distinct mf.pb_id, mf.exp,gf.go_id,d.name "
        "from microarray_fact mf "
        "inner join probe pf on pf.pb_id = mf.pb_id "
        "inner join gene_fact gf on pf.UID = gf.UID "
        "inner join clinical_fact cf on cf.s_id = mf.s_id "
        "inner join disease d on d.ds_id = cf.ds_id "
        "where gf.go_id = '" + go_id + "' and d.name='" + disease_name + "'")
    conn_data2.execute(
        "select  distinct mf.pb_id, mf.exp,gf.go_id,d.name "
        "from microarray_fact mf "
        "inner join probe pf on pf.pb_id = mf.pb_id "
        "inner join gene_fact gf on pf.UID = gf.UID "
        "inner join clinical_fact cf on cf.s_id = mf.s_id "
        "inner join disease d on d.ds_id = cf.ds_id "
        "where gf.go_id = '" + go_id + "' and d.name!='" + disease_name + "'")

    data1 = conn_data1.fetchall()
    data2 = conn_data2.fetchall()

    group_with_disease = []
    group_without_disease = []

    for row in data1:
        group_with_disease.append(row[1])

    for row in data2:
        group_without_disease.append(row[1])

    x = ttest_ind(group_with_disease, group_without_disease, equal_var=True)

    return x
