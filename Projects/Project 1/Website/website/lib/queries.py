import pymysql as mysql
from scipy.stats import ttest_ind


def three_1(disease_name):
    conn = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')
    conn2 = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')

    cursor_group_a = conn.cursor()
    cursor_group_b = conn2.cursor()

    cursor_group_a.execute(
        "select distinct gf.uid,mf.exp, patient.p_id"
        "from gene_fact gf"
        "join probe p on p.UID = gf.UID"
        "join microarray_fact mf on mf.pb_id = p.pb_id"
        "join clinical_fact cf on cf.s_id = mf.s_id"
        "join disease d on d.ds_id = cf.ds_id"
        "join patient on patient.p_id = cf.p_id"
        "where d.name = '" + disease_name + "'")

    cursor_group_b.execute(
        "select distinct gf.uid,mf.exp, patient.p_id"
        "from gene_fact gf"
        "join probe p on p.UID = gf.UID"
        "join microarray_fact mf on mf.pb_id = p.pb_id"
        "join clinical_fact cf on cf.s_id = mf.s_id"
        "join disease d on d.ds_id = cf.ds_id"
        "join patient on patient.p_id = cf.p_id"
        "where d.name != '" + disease_name + "'")

    data_a = cursor_group_a.fetchall()
    data_b = cursor_group_b.fetchall()

    l1 = []
    l2 = []

    d1 = dict()
    d2 = dict()

    for row in data_a:
        l1.append(row[0])
        uid1 = row[0]
        exp1 = row[1]

        d1.setdefault(uid1, []).append(exp1)

    for row in data_b:
        l2.append(row[0])
        uid2 = row[0]
        exp2 = row[1]

        d2.setdefault(uid2, []).append(exp2)

    if_gene = []
    for key in d1:
        x = d1[key]
        y = d2[key]
        z = ttest_ind(x, y, equal_var=True)
        if z[1] < 0.01:
            if_gene.append(key)

    return if_gene


def three_2():
    return True


def two_1():
    return True


def two_2():
    return True


def two_3():
    return True


def two_4(go_id, disease_name):
    conn1 = mysql.connect(user='root', password='-----', host='localhost', database='cse601-project1')
    conn2 = mysql.connect(user='root', password='----', host='localhost', database='cse601-project1')

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


def two_5(go_id,diseases):
    conn = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')


    disease_lists = [[]] * len(diseases)




    cursor = conn.cursor()

    cursor.execute(
        "select distinct  pf.pb_id,mf.exp "
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


def two_6():
    return True
