from Exceptions.exercise_count_exception import ExerciseCountException
from aplication import app
from flask import jsonify, Response
from flask_restful import Resource
from Services.dayofweekExercisesServices import DayofweekExercisesService
from Models.Transfer.dayofweekExercisesnameDo import DayofweekExercisesDo
from Controllers.exerciseController import _exerciseService
from Controllers.dayofweekController import _dayofweekService
from Exceptions.dayofweek_not_found_exception import DayofweekNotFoundException
from Exceptions.exercise_not_found_exception import ExerciseNotFoundException
from logger import service_logger
from Exceptions.problemDetails import ProblemDetails
from Exceptions.exercise_in_dayofweek_exception import ExerciseInDayofweekException

_dayofweekExercisesService = DayofweekExercisesService()


class DayofweekExercisesController(Resource):
    @staticmethod
    @app.route('/dc/v1/dayofweek/<int:dayofweek_id>/exercises', methods=['GET'])
    def get_dayofweek_exercises(dayofweek_id):
        try:
            _dayofweekService.findDayofweek(dayofweek_id)

            dayofweek_exerc = []
            raw = _dayofweekExercisesService.findAllDayofweekExercises(dayofweek_id)
            for item in raw:
                dayofweek_exerc_do = DayofweekExercisesDo(
                    id= item.Exercise.id,
                    ExerciseName= item.Exercise.ExerciseName,
                    Classroom= item.Exercise.Classroom
                )
                dayofweek_exerc.append(dayofweek_exerc_do)
            return jsonify({"dayofweek_exerc": dayofweek_exerc})

        except DayofweekNotFoundException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка поиска сущности DayofweekExercisesController",
                title=exp.message,
                status=404,
                detail="Запрашиваемый id дня недели не найден",
                instance="http://127.0.0.1:3000/dc/v1/dayofweek/<int:dayofweek_id>/exercises"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 404

    @staticmethod
    @app.route('/dc/v1/dayofweek/<int:dayofweek_id>/exercise/<int:exercise_id>', methods=['GET'])
    def get_dayofweek_exercise(dayofweek_id, exercise_id):
        try:
            _dayofweekService.findDayofweek(dayofweek_id)
            _exerciseService.findExercise(exercise_id)

            raw = _dayofweekExercisesService.findDayofweekExercise(dayofweek_id, exercise_id)
            dayofweek_exerc_do = DayofweekExercisesDo(
                    id= raw.Exercise.id,
                    ExerciseName= raw.Exercise.ExerciseName,
                    Classroom= raw.Exercise.Classroom
                )
            return jsonify(dayofweek_exerc_do)

        except DayofweekNotFoundException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка поиска сущности DayofweekExercisesController",
                title=exp.message,
                status=404,
                detail="Запрашиваемый id дня недели не найден",
                instance="http://127.0.0.1:3000/dc/v1/dayofweek/<int:dayofweek_id>/exercises/<int:exercise_id>"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 404

        except ExerciseNotFoundException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка поиска сущности DayofweekExercisesController",
                title=exp.message,
                status=404,
                detail="Запрашиваемый id занятия не найден",
                instance="http://127.0.0.1:3000/dc/v1/dayofweek/<int:dayofweek_id>/exercises/<int:exercise_id>"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 404

        except ExerciseInDayofweekException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка поиска сущности DayofweekExercisesController",
                title=exp.message,
                status=404,
                detail="Запрашиваемый id занятия в этом дне не найден",
                instance="http://127.0.0.1:3000/dc/v1/dayofweek/<int:dayofweek_id>/exercises/<int:exercise_id>"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 404



    @staticmethod
    @app.route('/dc/v1/dayofweek/<int:dayofweek_id>/add_exercise/<int:exercise_id>', methods=['POST'])
    def add_dayofweek_exercises(dayofweek_id, exercise_id):
        try:
            _dayofweekService.findDayofweek(dayofweek_id)
            _exerciseService.findExercise(exercise_id)
            _dayofweekExercisesService.addDayofweekExercise(dayofweek_id, exercise_id)

            dayofweek_discs = []
            raw = _dayofweekExercisesService.findAllDayofweekExercises(dayofweek_id)
            for item in raw:
                dayofweek_disc_do = DayofweekExercisesDo(
                    id=item.Exercise.id,
                    ExerciseName=item.Exercise.ExerciseName,
                    Classroom=item.Exercise.Classroom
                )
                dayofweek_discs.append(dayofweek_disc_do)
            return ({"dayofweek_disc_do": dayofweek_discs})

        except DayofweekNotFoundException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка поиска сущности DayofweekExercisesController",
                title=exp.message,
                status=404,
                detail="Запрашиваемый id дня недели не найден",
                instance="http://127.0.0.1:3000/dc/v1/dayofweek/<int:dayofweek_id>/add_exercise/<int:exercise_id>"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 404

        except ExerciseNotFoundException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка поиска сущности DayofweekExercisesController",
                title=exp.message,
                status=404,
                detail="Запрашиваемый id занятия не найден",
                instance="http://127.0.0.1:3000/dc/v1/dayofweek/<int:dayofweek_id>/add_exercise/<int:exercise_id>"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 404

        except ExerciseCountException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка добавления сущности DayofweekExercisesController",
                title=exp.message,
                status=403,
                detail="В одном дне не может быть больше 8 уроков",
                instance="http://127.0.0.1:3000/dc/v1/dayofweek/<int:dayofweek_id>/add_exercise/<int:exercise_id>"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 403

    @staticmethod
    @app.route('/dc/v1/dayofweek/<int:dayofweek_id>/delete_exercise/<int:exercise_id>', methods=['DELETE'])
    def delete_dayofweek_exercise(dayofweek_id, exercise_id):
        try:

            _dayofweekService.findDayofweek(dayofweek_id)
            _exerciseService.findExercise(exercise_id)
            _dayofweekExercisesService.findDayofweekExercise(dayofweek_id, exercise_id)

            _dayofweekExercisesService.deleteDayofweekExercise(dayofweek_id, exercise_id)
            return jsonify('Удален')

        except DayofweekNotFoundException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка поиска сущности DayofweekExercisesController",
                title=exp.message,
                status=404,
                detail="Запрашиваемый id дня недели не найден",
                instance="http://127.0.0.1:3000/dc/v1/dayofweek/<int:dayofweek_id>/delete_exercise/<int:exercise_id>"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 404

        except ExerciseNotFoundException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка поиска сущности DayofweekExercisesController",
                title=exp.message,
                status=404,
                detail="Запрашиваемый id занятия не найден",
                instance="http://127.0.0.1:3000/dc/v1/dayofweek/<int:dayofweek_id>/delete_exercise/<int:exercise_id>"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 404

        except ExerciseInDayofweekException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка поиска сущности DayofweekExercisesController",
                title=exp.message,
                status=404,
                detail="Запрашиваемый id занятия в этом дне не найден",
                instance="http://127.0.0.1:3000/dc/v1/dayofweek/<int:dayofweek_id>/delete_exercise/<int:exercise_id>"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 404


