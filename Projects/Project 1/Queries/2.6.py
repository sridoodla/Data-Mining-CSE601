import pymysql as mysql
import scipy
from scipy.stats import ttest_ind


def two_6(go_id, disease_1, disease_2):
    conn1 = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')
    conn2 = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')

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
            a, b = scipy.stats.pearsonr(x, y)
            sum_exp_d1_d2 += a

    done_keys = []

    # N1 * (N1-1)/2 pearson correlations for Disease 1 vs Disease 1
    for key1_all in d1:
        done_keys.append(key1_all)
        x = d1[key1_all]
        for key2_all in d1:
            if key2_all not in done_keys:
                y = d1[key2_all]
                c, d = scipy.stats.pearsonr(x, y)
                sum_exp_d1_d1 += c

    size_d1_d1 = len(d1) * (len(d1) - 1) / 2
    size_d1_d2 = len(d1) * len(d2)

    result = [sum_exp_d1_d1 / size_d1_d1, sum_exp_d1_d2 / size_d1_d2]

    print(result)
    return result


two_6(7154, 'ALL', 'AML')
