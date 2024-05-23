import sqlite3
from Models.dayofweekname import Dayofweek
from Exceptions.dayofweek_not_found_exception import DayofweekNotFoundException
from Exceptions.dayofweek_dublicate_exception import DayofweekDublicateException
con = sqlite3.connect('exercise_service.db', check_same_thread=False)

class DayofweekService:


    def findDayofweek(self, id):
        with con:
            sql_select = """SELECT  
                            id, 
                            dayofweek_name
                            FROM dayofweek 
                            WHERE id = ?"""

            raw_dayofweek = con.execute(sql_select, (id,)).fetchone()
            if raw_dayofweek == None:
                raise DayofweekNotFoundException("Такой день недели не найден")

            dayofweek = Dayofweek()
            dayofweek.id = raw_dayofweek[0]
            dayofweek.DayofweekName = raw_dayofweek[1]

        return dayofweek


    def findAllDayofweeks(self):

        dayofweeks = []
        with con:
            sql_select = """SELECT  id, 
                            dayofweek_name
                            FROM dayofweek"""
            raw_dayofweek = con.execute(sql_select).fetchall()

            for row in raw_dayofweek:
                dayofweek = {
                    "id": row[0],
                    "DayofweekName": row[1]
                }
                dayofweeks.append(dayofweek)

        return dayofweeks


    def deleteDayofweek(self, id):
        with con:
            sql_delete_exercises = """DELETE FROM dayofweek_exercise WHERE dayofweek_id = ?"""
            con.execute(sql_delete_exercises, (id,))

            sql_delete = """DELETE  
                            FROM 
                                dayofweek 
                            WHERE id = ?"""
            con.execute(sql_delete, (id,))

        return id

    def addDayofweek(self, dayofweek_object: Dayofweek):
        with con:
            with con:
                sql_search = """SELECT * FROM dayofweek 
                                WHERE dayofweek_name = ?"""

                searchResult = con.execute(sql_search, (dayofweek_object.DayofweekName,)).fetchone()
                if searchResult is not None:
                    raise DayofweekDublicateException("Такой день недели уже есть")


            sql_insert = """INSERT INTO dayofweek 
                            (dayofweek_name) 
                             values(?)"""
            con.execute(sql_insert, (dayofweek_object.DayofweekName,))


    def updateDayofweek(self, id, dayofweek_object: Dayofweek):
        with con:
            sql_search = """SELECT * FROM dayofweek 
                            WHERE dayofweek_name = ?"""

            searchResult = con.execute(sql_search, (dayofweek_object.DayofweekName,)).fetchone()
            if searchResult is not None:
                raise DayofweekDublicateException("Такой день недели уже есть")


            sql_update = """UPDATE dayofweek 
                            SET 
                            dayofweek_name = ?
                            WHERE id = ?"""
            con.execute(sql_update, (dayofweek_object.DayofweekName, id))