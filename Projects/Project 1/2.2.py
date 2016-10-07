import pymysql as mysql


def two_2(column_name, column_value):
    conn = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')

    cursor = conn.cursor()

    cursor.execute("select distinct drug.type "
                   "from drug "
                   "INNER JOIN clinical_fact ON drug.dr_id = clinical_fact.dr_id "
                   "inner join disease on disease.ds_id = clinical_fact.ds_id "
                   "where disease." + column_name + " = '" + column_value + "'")

    data = cursor.fetchall()

    return data


two_2('type', 'leukemia')
