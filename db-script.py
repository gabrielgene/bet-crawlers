import psycopg2
import time

con = psycopg2.connect(host='0.0.0.0', database='bet-crawlers',
                       user='postgres', password='betcrawlers@321', port='1234')
cur = con.cursor()

# - rivalo_eventos
# evento_id
# esp_nome
# liga_nome
# camp_nome
# camp_url
# evento_data
# evento_hora
# evento_nome
# evento_casa
# evento_visitante
# evento_casa_odd
# evento_empate_odd
# evento_visitante_odd

sql = "create table rivalo_eventos (id serial primary key, esp_nome varchar(255)," \
    "liga_nome varchar(255), camp_nome varchar(255), camp_url varchar(255),"\
    "evento_data varchar(255), evento_hora varchar(255), evento_nome varchar(255)," \
    "evento_casa varchar(255), evento_visitante varchar(255), evento_casa_odd numeric (5, 2)," \
    "evento_empate_odd numeric (5, 2), evento_visitante_odd numeric (5, 2), data_insercao  timestamp with time zone not null default now())"
cur.execute(sql)
con.commit()

# - rivalo_poss
# poss_id
# evento_id
# mer_nome
# evento_nome
# poss_nome_1
# poss_valor_1
# poss_nome_2
# poss_valor_2
# poss_nome_3
# poss_valor_3

sql = "create table rivalo_mercados (id serial primary key, evento_id integer REFERENCES rivalo_eventos (id)," \
    "mer_nome varchar(255), home_odd numeric (5, 2), empate_odd numeric (5, 2), visitante_odd numeric (5, 2)," \
    "evento_nome varchar(255), esp_nome varchar(255), poss_nome_1 varchar(255), poss_valor_1 numeric (5, 2)," \
    "poss_nome_2 varchar(255), poss_valor_2 numeric (5, 2)," \
    "poss_nome_3 varchar(255), poss_valor_3 numeric (5, 2), data_insercao  timestamp with time zone not null default now())"
cur.execute(sql)
con.commit()

# sql = "insert into rivalo_eventos values (default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# sql = "insert into rivalo_mercados values (default, %s, %s, %s, %s, %s, %s, %s, %s)"

con.commit()
con.close()
