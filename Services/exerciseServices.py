import sqlite3
from Models.exercisename import Exercise
from Exceptions.exercise_not_found_exception import ExerciseNotFoundException
from Exceptions.exercise_dublicate_exception import ExerciseDublicateException

con = sqlite3.connect('exercise_service.db', check_same_thread=False)
class ExerciseService:


    def findExercise(self, id):
        with con:
            sql_select = """SELECT  
                            id, 
                            exercise_name, 
                            сlassroom 
                            FROM exercise 
                            WHERE id = ?"""

            raw_exercise = con.execute(sql_select, (id,)).fetchone()
            if raw_exercise == None:
                raise ExerciseNotFoundException("Такое занятие не найдено")
            exercise = Exercise()
            exercise.id = raw_exercise[0]
            exercise.ExerciseName = raw_exercise[1]
            exercise.Classroom = raw_exercise[2]
        return exercise


    def findAllExercises(self):

        exercises = []
        with con:
            sql_select = """SELECT  id, 
                            exercise_name,  
                            сlassroom 
                            FROM exercise"""
            raw_exercises = con.execute(sql_select).fetchall()

            for row in raw_exercises:
                exercise = {
                    "id": row[0],
                    "ExerciseName": row[1],
                    "Classroom": row[2]
                }
                exercises.append(exercise)

        return exercises


    def deleteExercise(self, id):
        with con:
            sql_delete = """DELETE  
                            FROM 
                                exercise 
                            WHERE id = ?"""

            con.execute(sql_delete, (id,))
        return id

    def addExercise(self, exercise_object: Exercise):
        with con:
            sql_search = """SELECT * FROM exercise 
                            WHERE exercise_name = ? AND сlassroom = ?"""

            searchResult = con.execute(sql_search, (exercise_object.ExerciseName, exercise_object.Classroom)).fetchone()
            if searchResult is not None:
                raise ExerciseDublicateException("Такое занятие в этом кабинете уже есть")

            sql_insert = """INSERT INTO exercise 
                            (exercise_name, сlassroom) 
                             values(?, ?)"""
            con.execute(sql_insert, (exercise_object.ExerciseName,
                                     exercise_object.Classroom))

    def updateExercise(self, id, exercise_object: Exercise):
        with con:
            sql_search = """SELECT * FROM exercise 
                            WHERE exercise_name = ? AND сlassroom = ?"""

            searchResult = con.execute(sql_search, (exercise_object.ExerciseName, exercise_object.Classroom)).fetchone()
            if searchResult is not None:
                raise ExerciseDublicateException("Такое занятие в этом кабинете уже есть")
            sql_update = """UPDATE exercise 
                            SET 
                            exercise_name = ?, 
                            сlassroom = ? 
                            WHERE id = ?"""

            con.execute(sql_update, (exercise_object.ExerciseName, exercise_object.Classroom, id))
