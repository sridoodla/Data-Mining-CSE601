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
