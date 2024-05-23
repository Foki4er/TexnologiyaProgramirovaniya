import sqlite3
from Models.exercisename import Exercise
from Models.dayofweekname import Dayofweek
from Models.dayofweekExercisesname import DayofweekExercises
from aplication import con
from Exceptions.exercise_count_exception import ExerciseCountException
from Exceptions.exercise_in_dayofweek_exception import ExerciseInDayofweekException
class DayofweekExercisesService:
    def findAllDayofweekExercises(self, dayofweek_id):
        dayofweek_exercs = []
        with con:
            sql_select = """SELECT
                              e.id,
                              e.exercise_name,
                              e.сlassroom,
                              d.id,
                              d.dayofweek_name,
                              de.id
                            FROM
                              dayofweek d,
                              exercise e,
                              dayofweek_exercise de
                            WHERE
                              d.id = de.dayofweek_id
                              AND e.id = de.exercise_id
                              AND d.id = ?"""
            raw_exercises = con.execute(sql_select, [dayofweek_id]).fetchall()
            for row in raw_exercises:
                exercise = Exercise(
                    id=row[0],
                    ExerciseName=row[1],
                    Classroom=row[2]
                )
                dayofweek = Dayofweek(
                    id=row[0],
                    DayofweekName=row[1]
                )
                dayofweek_exerc = DayofweekExercises(
                    id= row[0],
                    Dayofweek= dayofweek,
                    Exercise= exercise
                )
                dayofweek_exercs.append(dayofweek_exerc)

        return dayofweek_exercs

    def findDayofweekExercise(self, dayofweek_id, exercise_id):
        with con:
            sql_select = """SELECT
                              d.id,
                              e.exercise_name,
                              e.сlassroom,
                              de.id
                            FROM
                              dayofweek d,
                              exercise e,
                              dayofweek_exercise de
                            WHERE
                              d.id = de.dayofweek_id
                              AND e.id = de.exercise_id
                              AND d.id = ?
                              AND e.id =?"""
            raw_exercises = con.execute(sql_select, [dayofweek_id, exercise_id]).fetchone()
            if raw_exercises == None:
                raise ExerciseInDayofweekException("Занятия с таким id нет у этого дня")
            exercise = Exercise(
                id=raw_exercises[0],
                ExerciseName=raw_exercises[1],
                Classroom=raw_exercises[2]
            )
            dayofweek = Dayofweek(
                id=raw_exercises[0],
                DayofweekName=raw_exercises[1]
            )
            dayofweek_exerc = DayofweekExercises(
                id= raw_exercises[0],
                Exercise= exercise,
                Dayofweek= dayofweek
            )
        return dayofweek_exerc

    def addDayofweekExercise(self, dayofweek_id, exercise_id):
        with con:
            discs = self.findAllDayofweekExercises(dayofweek_id)

            if len(discs) >= 8:
                raise ExerciseCountException("Нельзя добавить больше 8 уроков в день")

            sql_insert = """INSERT INTO dayofweek_exercise
                                   (dayofweek_id, exercise_id) 
                                   values (?, ?)"""
            con.execute(sql_insert, [dayofweek_id, exercise_id])

    def deleteDayofweekExercise(self, dayofweek_id, exercise_id):
        with con:
            sql_delete = """DELETE 
                            FROM
                              dayofweek_exercise
                            WHERE dayofweek_id = ?
                            AND exercise_id = ?"""
            con.execute(sql_delete, [dayofweek_id,exercise_id])
        return id