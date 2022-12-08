import json
import pymysql

def direct_hit(master_private_dns):
    conn = pymysql.connect(host=master_private_dns,
                           user="sbtest", password="passw0rd",
                           db="sakila")
    cur = conn.cursor()
    cur.execute("select * from actor")
    output = cur.fetchall()
    print(output)
