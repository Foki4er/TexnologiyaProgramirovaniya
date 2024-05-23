from Services.dbCreatorService import Connection
from Controllers.exerciseController import exerciseController
from Controllers.dayofweekController import dayofweekController
from aplication import  app, api
from Controllers.reportController import ReportController
from Controllers.dayofweekExercisesController import DayofweekExercisesController

if __name__ == "__main__":
    con = Connection()
    con.connect()
    api.add_resource(exerciseController)
    api.add_resource(dayofweekController)
    api.add_resource(ReportController)
    api.add_resource(DayofweekExercisesController)

    app.run(debug=True, port=3000, host="127.0.0.1")