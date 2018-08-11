import psycopg2
import time

con = psycopg2.connect(host='0.0.0.0', database='bet-crawlers',
                       user='postgres', password='betcrawlers@321', port='1234')
cur = con.cursor()

sql = "create table test_bet (id serial primary key, nome_1 varchar(100), nome_2 varchar(100))"
cur.execute(sql)

sql = "insert into test_bet values (default, %s, %s)"
cur.execute(sql, ('nome1', 'nome2'))
cur.execute(sql, ('nome1', 'nome2'))
cur.execute(sql, ('nome1', 'nome2'))
cur.execute(sql, ('nome1', 'nome2'))
cur.execute(sql, ('nome1', 'nome2'))
cur.execute(sql, ('nome1', 'nome2'))
cur.execute(sql, ('nome1', 'nome2'))
cur.execute(sql, ('nome1', 'nome2'))
cur.execute(sql, ('nome1', 'nome2'))

con.commit()
con.close()
