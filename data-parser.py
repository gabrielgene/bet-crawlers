import json
import psycopg2
import time
con = psycopg2.connect(host='172.17.0.2', database='bet-data-dev',
                       user='postgres', password='deb@00')

cur = con.cursor()

# sql = "create table aposta_bet (id serial primary key, casa varchar(100), visitante varchar(100)," \
#     "casa_odd varchar(20), empate_odd varchar(20), visitante_odd varchar(20), debug varchar(900))"
# cur.execute(sql)

# sql = "create table scout_bet (id serial primary key, name varchar(100), data varchar(900), aposta_id integer REFERENCES aposta_bet (id))"
# cur.execute(sql)

with open('debug.json') as f:
    data = json.load(f)

list_of_bets = data["football-germany-amateur"]

i = 0

for bet in list_of_bets:
    # if i > 30:
    #     break
    home = bet["home"]
    visitant = bet["visitant"]
    home_odd = bet["home_odd"]
    draw_odd = bet["draw_odd"]
    visitant_odd = bet["visitant_odd"]
    debug_list = bet["debug"]
    debug = ' - '.join(str(i) for i in debug_list)
    print('>>>>>>>>>>>>>>>>>>> HOME')
    print(debug)

    # sql = "insert into aposta_bet values (default, '{}', '{}', '{}', '{}', '{}', '{}')".format(home, visitant, home_odd, draw_odd, visitant_odd, debug)
    sql = "insert into aposta_bet values (default, %s, %s, %s, %s, %s, %s) RETURNING id"
    # print(sql)
    cur.execute(sql, (home, visitant, home_odd, draw_odd,
                      visitant_odd, debug))
    id_of_new_row = cur.fetchone()[0]
    print(id_of_new_row)

    scout_list = bet["scout_rows"]

    for idx, scout in enumerate(scout_list):
        scout_name = scout[0]
        scout_list = scout[1:]
        scout_data = ' - '.join(str(i) for i in scout_list)
        # print('>>>>>>>>>>>>>>>>>>>> SCOUT')
        # print(scout_name)
        # print(scout_data)
        sql = "insert into scout_bet values (default, %s, %s, %s)"
        # sql = "insert into scout_bet values (default, '{}', '{}', {})".format(scout_name, scout_data, idx)
        # print(sql)
        sql = "insert into scout_bet values (default, %s, %s, %s)"
        cur.execute(sql, (scout_name, scout_data, id_of_new_row))

    i = i + 1

con.commit()
con.close()
