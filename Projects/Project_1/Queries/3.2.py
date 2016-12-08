import pymysql as mysql
import scipy
from scipy.stats import ttest_ind


def three_2(disease_name):
    conn1 = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')
    conn2 = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')
    conn3 = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')
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
            a, b = scipy.stats.pearsonr(all_on_patient[patientKey], test_patient[i])
            all_vs_test.append(a)
        for patientKey in not_all_on_patient:
            c, d = scipy.stats.pearsonr(not_all_on_patient[patientKey], test_patient[i])
            not_all_vs_test.append(c)

        t_test_results = ttest_ind(all_vs_test, not_all_vs_test)

        if t_test_results[1] < 0.01:
            positive.append(i)
        else:
            negative.append(i)

    return [positive, negative]


three_2('AML')
