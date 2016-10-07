import pymysql as mysql


def two_1(column_name, column_value):
    conn = mysql.connect(user='root', password='09071992', host='localhost', database='cse601-project1')

    cursor = conn.cursor()

    cursor.execute("select count(DISTINCT p_id) "
                   "from clinical_fact "
                   "join disease on clinical_fact.ds_id = disease.ds_id "
                   "where disease." + column_name + " = '" + column_value + "'")

    data = cursor.fetchall()

    return data[0][0]


two_1('type', 'leukemia')
