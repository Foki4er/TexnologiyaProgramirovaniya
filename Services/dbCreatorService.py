import sqlite3

from aplication import  con


class Connection:
    def createTable(self): #открываем базу
        with con: # получаем количество таблиц с нужным нам именем
            data = con.execute("""select count(*) from sqlite_master where type='table' and name='exercise'""")
            for row in data: # если таких таблиц нет
                if row[0] == 0: # создаём таблицу для преподавателей
                    with con:
                        con.execute(""" 
                            CREATE TABLE exercise ( 
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                exercise_name TEXT, 
                                сlassroom INTEGER
                            ); 
                        """)
        # получаем количество таблиц с нужным нам именем
            data2 = con.execute("""select count(*) from sqlite_master where type='table' and name='dayofweek'""")
            for row in data2: # если таких таблиц нет
                if row[0] == 0: # создаём таблицу для преподавателей
                    with con:
                        con.execute(""" 
                            CREATE TABLE dayofweek ( 
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                dayofweek_name TEXT
                            ); 
                        """)
         # получаем количество таблиц с нужным нам именем
            data3 = con.execute("""select count(*) from sqlite_master where type='table' and name='dayofweek_exercise'""")
            for row in data3: # если таких таблиц нет
                if row[0] == 0: # создаём таблицу для преподавателей
                    with con:
                        con.execute(""" 
                                    CREATE TABLE dayofweek_exercise ( 
                                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    dayofweek_id INTEGER,
                                    exercise_id INTEGER,
                                    FOREIGN KEY (dayofweek_id) REFERENCES dayofweek(id),
                                     FOREIGN KEY (exercise_id) REFERENCES exercise(id)
                                    ); 
                        """)


    def connect(self):
        self.createTable()

