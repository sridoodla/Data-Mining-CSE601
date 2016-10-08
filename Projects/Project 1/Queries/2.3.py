import pymysql as mysql


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

    print(data)
    return data


two_3('aml', '1', '2')
