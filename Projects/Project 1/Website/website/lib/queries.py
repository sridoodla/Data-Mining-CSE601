import pymysql as mysql
from scipy.stats import ttest_ind, stats


def three_1(disease_name):
    conn = mysql.connect(user='root', password='Seagate47!', host='localhost', database='cse601-project1')
    conn2 = mysql.connect(user='root', password='Seagate47!', host='localhost', database='cse601-project1')

    cursor_group_a = conn.cursor()
    cursor_group_b = conn2.cursor()

    query_a = "select distinct patient.p_id,gf.uid,mf.exp " \
              "from gene_fact gf " \
              "join probe p on p.UID = gf.UID " \
              "join microarray_fact mf on mf.pb_id = p.pb_id " \
              "join clinical_fact cf on cf.s_id = mf.s_id " \
              "join disease d on d.ds_id = cf.ds_id " \
              "join patient on patient.p_id = cf.p_id " \
              "where d.name = '" + disease_name + "'"
    cursor_group_a.execute(query_a)

    query_b = "select distinct patient.p_id,gf.uid,mf.exp " \
              "from gene_fact gf " \
              "join probe p on p.UID = gf.UID " \
              "join microarray_fact mf on mf.pb_id = p.pb_id " \
              "join clinical_fact cf on cf.s_id = mf.s_id " \
              "join disease d on d.ds_id = cf.ds_id " \
              "join patient on patient.p_id = cf.p_id " \
              "where d.name != '" + disease_name + "'"

    cursor_group_b.execute(query_b)

    data_a = cursor_group_a.fetchall()
    data_b = cursor_group_b.fetchall()

    print(data_a)
    print(data_b)

    l1 = []
    l2 = []

    d1 = dict()
    d2 = dict()

    for row in data_a:
        l1.append(row[1])
        uid1 = row[1]
        exp1 = row[2]

        d1.setdefault(uid1, []).append(exp1)

    for row in data_b:
        l2.append(row[1])
        uid2 = row[1]
        exp2 = row[2]

        d2.setdefault(uid2, []).append(exp2)

    if_gene = []
    for key in d1:
        x = d1[key]
        y = d2[key]
        z = ttest_ind(x, y, equal_var=True)
        if z[1] < 0.01:
            if_gene.append(key)

    print(if_gene)
    print(len(if_gene))


def three_2():
    return True


def two_1(column_name, column_value):
    conn = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')

    cursor = conn.cursor()

    cursor.execute("select count(DISTINCT p_id) "
                   "from clinical_fact "
                   "join disease on clinical_fact.ds_id = disease.ds_id "
                   "where disease." + column_name + " = '" + column_value + "'")

    data = cursor.fetchall()

    return data[0][0]


def two_2(column_name, column_value):
    conn = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')

    cursor = conn.cursor()

    cursor.execute("select distinct drug.type "
                   "from drug "
                   "INNER JOIN clinical_fact ON drug.dr_id = clinical_fact.dr_id "
                   "inner join disease on disease.ds_id = clinical_fact.ds_id "
                   "where disease." + column_name + " = '" + column_value + "'")

    result = cursor.fetchall()

    data = []

    for row in result:
        data.append(row[0])

    return data


def two_3(ds_name, mu_id, cl_id):
    conn = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')

    cursor = conn.cursor()

    cursor.execute("select distinct mf.exp from microarray_fact mf "
                   "inner join clinical_fact cf on mf.s_id = cf.s_id "
                   "inner join disease ds on cf.ds_id = ds.ds_id "
                   "inner join probe on probe.pb_id = mf.pb_id "
                   "inner join gene_fact gf on gf.UID = probe.UID "
                   "where ds.name = '" + ds_name + "' "
                                                   "AND mf.mu_id = " + str(mu_id) + " "
                                                                                    "AND gf.cl_id = " + str(
        cl_id) + " ")

    results = cursor.fetchall()
    data = []

    for row in results:
        data.append(row[0])

    return data


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


def two_5(go_id, diseases):
    conn = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')

    cursor = conn.cursor()

    cursor.execute("select distinct  mf.exp,d.name "
                   "from microarray_fact mf "
                   "inner join probe pf on pf.pb_id = mf.pb_id "
                   "inner join gene_fact gf on pf.UID = gf.UID "
                   "inner join clinical_fact cf on cf.s_id = mf.s_id "
                   "inner join disease d on d.ds_id = cf.ds_id "
                   "where gf.go_id = " + str(go_id) + " "
                                                      "and d.name = '" + diseases[0] + "' "
                                                                                       "union "
                                                                                       "select distinct  mf.exp,d.name "
                                                                                       "from microarray_fact mf "
                                                                                       "inner join probe pf on pf.pb_id = mf.pb_id "
                                                                                       "inner join gene_fact gf on pf.UID = gf.UID "
                                                                                       "inner join clinical_fact cf on cf.s_id = mf.s_id "
                                                                                       "inner join disease d on d.ds_id = cf.ds_id "
                                                                                       "where gf.go_id = " + str(
        go_id) + " and d.name = '" + diseases[1] + "' "
                                                   "union "
                                                   "select distinct  mf.exp,d.name "
                                                   "from microarray_fact mf "
                                                   "inner join probe pf on pf.pb_id = mf.pb_id "
                                                   "inner join gene_fact gf on pf.UID = gf.UID "
                                                   "inner join clinical_fact cf on cf.s_id = mf.s_id "
                                                   "inner join disease d on d.ds_id = cf.ds_id "
                                                   "where gf.go_id = " + str(go_id) + " and d.name = '" + diseases[
                       2] + "' "
                            "union "
                            "select distinct  mf.exp,d.name "
                            "from microarray_fact mf "
                            "inner join probe pf on pf.pb_id = mf.pb_id "
                            "inner join gene_fact gf on pf.UID = gf.UID "
                            "inner join clinical_fact cf on cf.s_id = mf.s_id "
                            "inner join disease d on d.ds_id = cf.ds_id "
                            "where gf.go_id = " + str(go_id) + " and d.name = '" + diseases[3] + "'")

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


def two_6():
    return True
