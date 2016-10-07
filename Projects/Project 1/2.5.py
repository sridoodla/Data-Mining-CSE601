import pymysql as mysql
import scipy.stats as stats


def two_5(go_id, diseases):

    conn = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')

    cursor = conn.cursor()

    cursor.execute("select distinct  mf.exp,d.name "
    "from microarray_fact mf "
    "inner join probe pf on pf.pb_id = mf.pb_id "
    "inner join gene_fact gf on pf.UID = gf.UID "
    "inner join clinical_fact cf on cf.s_id = mf.s_id "
    "inner join disease d on d.ds_id = cf.ds_id "
    "where gf.go_id = "+ str(go_id) +" "
    "and d.name = '"+ diseases[0] +"' "
    "union "
    "select distinct  mf.exp,d.name "
    "from microarray_fact mf "
    "inner join probe pf on pf.pb_id = mf.pb_id "
    "inner join gene_fact gf on pf.UID = gf.UID "
    "inner join clinical_fact cf on cf.s_id = mf.s_id "
    "inner join disease d on d.ds_id = cf.ds_id "
    "where gf.go_id = "+ str(go_id) +" and d.name = '"+ diseases[1] +"' "
    "union "
    "select distinct  mf.exp,d.name "
    "from microarray_fact mf "
    "inner join probe pf on pf.pb_id = mf.pb_id "
    "inner join gene_fact gf on pf.UID = gf.UID "
    "inner join clinical_fact cf on cf.s_id = mf.s_id "
    "inner join disease d on d.ds_id = cf.ds_id "
    "where gf.go_id = "+ str(go_id) +" and d.name = '"+ diseases[2] +"' "
    "union "
    "select distinct  mf.exp,d.name "
    "from microarray_fact mf "
    "inner join probe pf on pf.pb_id = mf.pb_id "
    "inner join gene_fact gf on pf.UID = gf.UID "
    "inner join clinical_fact cf on cf.s_id = mf.s_id "
    "inner join disease d on d.ds_id = cf.ds_id "
    "where gf.go_id = "+ str(go_id) +" and d.name = '"+ diseases[3] +"'")

    data = cursor.fetchall()

    disease_1 = []
    disease_2 = []
    disease_3 = []
    disease_4 = []

    for row in data:

        if row[1] == diseases[0]:
            disease_1.append(row[0])

        elif row[1] == diseases[1]:
            disease_3.append(row[0])

        elif row[1] == diseases[2]:
            disease_2.append(row[0])

        elif row[1] == diseases[3]:
            disease_4.append(row[0])

    x = stats.f_oneway(disease_1, disease_3, disease_2, disease_4)

    return x

disease_list = ['ALL', 'AML', 'Colon tumor', 'Breast tumor']

two_5(7154, disease_list)
