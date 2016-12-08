import pymysql as mysql
from scipy.stats import ttest_ind, stats


creds = {
    'user': 'root',
    'password': '09071992',  # Change this if necessary.
    'host': 'localhost',
    'database': 'cse601-project1'
}


def three_1(disease_name):
    conn = mysql.connect(user=creds['user'], password=creds['password'], host=creds['host'], database=creds['database'])
    conn2 = mysql.connect(user=creds['user'], password=creds['password'], host=creds['host'], database=creds['database'])

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

    d1 = dict()
    d2 = dict()

    for row in data_a:
        uid1 = row[1]
        exp1 = row[2]

        d1.setdefault(uid1, []).append(exp1)

    for row in data_b:
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

    return if_gene


def three_2(disease_name):
    conn1 = mysql.connect(user=creds['user'], password=creds['password'], host=creds['host'], database=creds['database'])
    conn2 = mysql.connect(user=creds['user'], password=creds['password'], host=creds['host'], database=creds['database'])
    conn3 = mysql.connect(user=creds['user'], password=creds['password'], host=creds['host'], database=creds['database'])
    cursor1 = conn1.cursor()
    cursor2 = conn2.cursor()
    cursor3 = conn3.cursor()

    query_a = "select distinct patient.p_id,gf.uid,mf.exp " \
              "from gene_fact gf " \
              "join probe p on p.UID = gf.UID " \
              "join microarray_fact mf on mf.pb_id = p.pb_id " \
              "join clinical_fact cf on cf.s_id = mf.s_id " \
              "join disease d on d.ds_id = cf.ds_id " \
              "join patient on patient.p_id = cf.p_id " \
              "where d.name = '" + disease_name + "'"
    cursor1.execute(query_a)

    query_b = "select distinct patient.p_id,gf.uid,mf.exp " \
              "from gene_fact gf " \
              "join probe p on p.UID = gf.UID " \
              "join microarray_fact mf on mf.pb_id = p.pb_id " \
              "join clinical_fact cf on cf.s_id = mf.s_id " \
              "join disease d on d.ds_id = cf.ds_id " \
              "join patient on patient.p_id = cf.p_id " \
              "where d.name != '" + disease_name + "'"

    cursor2.execute(query_b)

    data_a = cursor1.fetchall()
    data_b = cursor2.fetchall()

    l1 = []
    l2 = []

    d1 = dict()
    d2 = dict()

    all_on_patient = dict()
    not_all_on_patient = dict()

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

    for row in data_a:
        if row[1] in if_gene:
            all_on_patient.setdefault(row[0], []).append(row[2])

    for row in data_b:
        if row[1] in if_gene:
            not_all_on_patient.setdefault(row[0], []).append(row[2])

    # 1.get all records from temt sample which have geneid in if_gene
    test_patient = dict()
    for geneID in if_gene:
        cursor3.execute("select * from test_samples ts1 where ts1.UID =" + str(geneID))
        temp_data = cursor3.fetchall()
        for row in temp_data:
            test_patient.setdefault(1, []).append(row[1])
            test_patient.setdefault(2, []).append(row[2])
            test_patient.setdefault(3, []).append(row[3])
            test_patient.setdefault(4, []).append(row[4])
            test_patient.setdefault(5, []).append(row[5])

    positive = []
    negative = []

    for i in range(1, 6):
        all_vs_test = []
        not_all_vs_test = []
        for patientKey in all_on_patient:
            a, b = stats.pearsonr(all_on_patient[patientKey], test_patient[i])
            all_vs_test.append(a)
        for patientKey in not_all_on_patient:
            c, d = stats.pearsonr(not_all_on_patient[patientKey], test_patient[i])
            not_all_vs_test.append(c)

        t_test_results = ttest_ind(all_vs_test, not_all_vs_test)

        if t_test_results[1] < 0.01:
            positive.append(i)
        else:
            negative.append(i)

    return [positive, negative]


def two_1(column_name, column_value):
    conn = mysql.connect(user=creds['user'], password=creds['password'], host=creds['host'], database=creds['database'])

    cursor = conn.cursor()

    cursor.execute("select count(DISTINCT p_id) "
                   "from clinical_fact "
                   "join disease on clinical_fact.ds_id = disease.ds_id "
                   "where disease." + column_name + " = '" + column_value + "'")

    data = cursor.fetchall()

    return data[0][0]


def two_2(column_name, column_value):
    conn = mysql.connect(user=creds['user'], password=creds['password'], host=creds['host'], database=creds['database'])

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
    conn = mysql.connect(user=creds['user'], password=creds['password'], host=creds['host'], database=creds['database'])

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
    conn1 = mysql.connect(user=creds['user'], password=creds['password'], host=creds['host'], database=creds['database'])
    conn2 = mysql.connect(user=creds['user'], password=creds['password'], host=creds['host'], database=creds['database'])

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
    conn = mysql.connect(user=creds['user'], password=creds['password'], host=creds['host'], database=creds['database'])

    cursor = conn.cursor()

    cursor.execute("select distinct  mf.exp,d.name,p.p_id,gf.uid "
                   "from microarray_fact mf "
                   "inner join probe pf on pf.pb_id = mf.pb_id "
                   "inner join gene_fact gf on pf.UID = gf.UID "
                   "inner join clinical_fact cf on cf.s_id = mf.s_id "
                   "inner join disease d on d.ds_id = cf.ds_id "
                   "inner join patient p on p.p_id = cf.p_id "
                   "where gf.go_id = " + str(go_id) + " "
                                                      "and d.name = '" + diseases[0] + "' "
                                                                                       "union "
                                                                                       "select distinct  mf.exp,d.name,p.p_id,gf.uid "
                                                                                       "from microarray_fact mf "
                                                                                       "inner join probe pf on pf.pb_id = mf.pb_id "
                                                                                       "inner join gene_fact gf on pf.UID = gf.UID "
                                                                                       "inner join clinical_fact cf on cf.s_id = mf.s_id "
                                                                                       "inner join disease d on d.ds_id = cf.ds_id "
                                                                                       "inner join patient p on p.p_id = cf.p_id "
                                                                                       "where gf.go_id = " + str(
        go_id) + " and d.name = '" + diseases[1] + "' "
                                                   "union "
                                                   "select distinct  mf.exp,d.name,p.p_id,gf.uid "
                                                   "from microarray_fact mf "
                                                   "inner join probe pf on pf.pb_id = mf.pb_id "
                                                   "inner join gene_fact gf on pf.UID = gf.UID "
                                                   "inner join clinical_fact cf on cf.s_id = mf.s_id "
                                                   "inner join disease d on d.ds_id = cf.ds_id "
                                                   "inner join patient p on p.p_id = cf.p_id "
                                                   "where gf.go_id = " + str(go_id) + " and d.name = '" + diseases[
                       2] + "' "
                            "union "
                            "select distinct  mf.exp,d.name,p.p_id,gf.uid "
                            "from microarray_fact mf "
                            "inner join probe pf on pf.pb_id = mf.pb_id "
                            "inner join gene_fact gf on pf.UID = gf.UID "
                            "inner join clinical_fact cf on cf.s_id = mf.s_id "
                            "inner join disease d on d.ds_id = cf.ds_id "
                            "inner join patient p on p.p_id = cf.p_id "
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

    print(x)
    return x


def two_6(go_id, disease_1, disease_2):
    conn1 = mysql.connect(user=creds['user'], password=creds['password'], host=creds['host'], database=creds['database'])
    conn2 = mysql.connect(user=creds['user'], password=creds['password'], host=creds['host'], database=creds['database'])

    cursor1 = conn1.cursor()
    cursor2 = conn2.cursor()

    cursor1.execute(
        "select distinct mf.pb_id, mf.exp,gf.go_id,d.name,cf.p_id,gf.uid "
        "from microarray_fact mf "
        "inner join probe pf on pf.pb_id = mf.pb_id "
        "inner join gene_fact gf on pf.UID = gf.UID "
        "inner join clinical_fact cf on cf.s_id = mf.s_id "
        "inner join disease d on d.ds_id = cf.ds_id "
        "where gf.go_id = " + str(go_id) + " and d.name='" + disease_1 + "'")

    cursor2.execute(
        "select distinct mf.pb_id, mf.exp,gf.go_id,d.name,cf.p_id,gf.uid "
        "from microarray_fact mf "
        "inner join probe pf on pf.pb_id = mf.pb_id "
        "inner join gene_fact gf on pf.UID = gf.UID "
        "inner join clinical_fact cf on cf.s_id = mf.s_id "
        "inner join disease d on d.ds_id = cf.ds_id "
        "where gf.go_id = " + str(go_id) + " and d.name='" + disease_2 + "'")

    data1 = cursor1.fetchall()
    data2 = cursor2.fetchall()

    d1 = dict()
    d2 = dict()

    for row in data1:
        exp = row[1]
        pid = row[4]
        d1.setdefault(pid, []).append(exp)

    for row in data2:
        exp = row[1]
        pid = row[4]
        d2.setdefault(pid, []).append(exp)

    sum_exp_d1_d2 = 0
    sum_exp_d1_d1 = 0

    # N1 * N2 pearson correlations for Disease 1 vs Disease 2
    for key_all in d1:
        x = d1[key_all]
        for key_notAll in d2:
            y = d2[key_notAll]
            a, b = stats.pearsonr(x, y)
            sum_exp_d1_d2 += a

    done_keys = []

    # N1 * (N1-1)/2 pearson correlations for Disease 1 vs Disease 1
    for key1_all in d1:
        done_keys.append(key1_all)
        x = d1[key1_all]
        for key2_all in d1:
            if key2_all not in done_keys:
                y = d1[key2_all]
                c, d = stats.pearsonr(x, y)
                sum_exp_d1_d1 += c

    size_d1_d1 = len(d1) * (len(d1) - 1) / 2
    size_d1_d2 = len(d1) * len(d2)

    result = [sum_exp_d1_d1 / size_d1_d1, sum_exp_d1_d2 / size_d1_d2]

    return result
