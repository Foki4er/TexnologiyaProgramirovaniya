import sqlite3
from Reports.exerciseReport import ExerciseReport
from Models.exercisename import Exercise


con = sqlite3.connect('exercise_service.db', check_same_thread=False)
_exerciseReport = ExerciseReport

class ReportService:
    def GenerateExerciseReport(self):
        exercises = []
        with con:
            sql_select = """SELECT id, 
                                exercise_name, 
                                сlassroom
                                FROM exercise"""

            raw_exercises = con.execute(sql_select).fetchall()
            for row in raw_exercises:
                exercise = { "id": row[0],
                            "ExerciseName": row[1],
                            "Classroom": row[2]
                             }

                exercises.append(exercise)

        return _exerciseReport.buid(exercises)
