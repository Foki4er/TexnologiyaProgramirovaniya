from flask import jsonify, request, Response
from flask_restful import Resource
from Models.exercisename import Exercise
from Services.exerciseServices import ExerciseService
from aplication import app
from Exceptions.exercise_not_found_exception import ExerciseNotFoundException
from Validators.exerciseValidator import ExerciseValidator
from jsonschema.exceptions import ValidationError
from Exceptions.problemDetails import ProblemDetails
from Exceptions.exercise_dublicate_exception import ExerciseDublicateException
from logger import service_logger

_exerciseService = ExerciseService()
_exerciseValidator = ExerciseValidator()


class exerciseController(Resource):
    @staticmethod
    @app.route ('/dc/v1/exercises', methods=['GET'])
    def get_exercises():
        return jsonify({"exercises": _exerciseService.findAllExercises()})

    @staticmethod
    @app.route('/dc/v1/exercise/<int:id>', methods=['GET'])
    def get_exercise(id):
        try:
            exercise = _exerciseService.findExercise(id)
            return jsonify(exercise)
        except ExerciseNotFoundException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка поиска сущности exerciseController",
                title=exp.message,
                status=404,
                detail="Запрашиваемый id занятия не найден",
                instance="http://127.0.0.1:3000/dc/v1/exercise"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 404


    @staticmethod
    @app.route('/dc/v1/delete_exercise/<int:id>', methods=['DELETE'])
    def delete_exercise(id):
        try:
            _exerciseService.findExercise(id)
            _exerciseService.deleteExercise(id)
            return jsonify(id)
        except ExerciseNotFoundException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка поиска сущности exerciseController",
                title=exp.message,
                status=404,
                detail="Запрашиваемый id занятия не найден",
                instance="http://127.0.0.1:3000/dc/v1/delete_exercise"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 404


    @staticmethod
    @app.route('/dc/v1/add_exercise', methods=['POST'])
    def add_exercise():
        try:
            request_data = request.get_json()
            _exerciseValidator.validate_exercise(request_data)
            exercise = Exercise()
            exercise.ExerciseName = request_data["ExerciseName"]
            exercise.Classroom = request_data["Classroom"]
            _exerciseService.addExercise(exercise)
            return jsonify({"exercises": _exerciseService.findAllExercises()})

        except ValidationError as err:
            problemDetails = ProblemDetails(
                type="Ошибка валидации в сущности exerciseController",
                title=err.message,
                status=400,
                detail="Отпрвленый JSON не соответствует схеме.",
                instance="http://127.0.0.1:3000/dc/v1/add_exercise"
            )
            res = f"{request_data}\n {err.message}\n {err.schema}"
            service_logger.error(res)
            return jsonify(problemDetails), 400

        except ExerciseDublicateException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка cоздания в сущности exerciseController",
                title=exp.message,
                status=409,
                detail="Данные отпрвленые в JSON уже есть в БД",
                instance="http://127.0.0.1:3000/dc/v1/add_exercise"
            )
            res = f"{request_data}\n {exp.message}"
            service_logger.error(res)
            return jsonify(problemDetails), 409


    @staticmethod
    @app.route('/dc/v1/update_exercise/<int:id>', methods=['PUT'])
    def update_exercise(id):
        try:
            _exerciseService.findExercise(id)

            request_data = request.get_json()
            _exerciseValidator.validate_exercise(request_data)

            exercise = Exercise()
            exercise.ExerciseName = request_data["ExerciseName"]
            exercise.Classroom = request_data["Classroom"]

            _exerciseService.updateExercise(id, exercise)
            return jsonify({"exercises": _exerciseService.findAllExercises()})

        except ValidationError as err:
            problemDetails = ProblemDetails(
                type="Ошибка валидации в сущности exerciseController",
                title=err.message,
                status=400,
                detail="Отпрвленый JSON не соответствует схеме.",
                instance="http://127.0.0.1:3000/dc/v1/update_exercise"
            )
            res = f"{request_data}\n {err.message}\n {err.schema}"
            service_logger.error(res)
            return jsonify(problemDetails), 400

        except ExerciseNotFoundException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка поиска сущности exerciseController",
                title=exp.message,
                status=404,
                detail="Запрашиваемый id занятия не найден",
                instance="http://127.0.0.1:3000/dc/v1/update_exercise"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 404

        except ExerciseDublicateException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка обновления в сущности exerciseController",
                title=exp.message,
                status=409,
                detail="Данные отпрвленые в JSON уже есть в БД",
                instance="http://127.0.0.1:3000/dc/v1/update_exercise"
            )
            res = f"{request_data}\n {exp.message}"
            service_logger.error(res)
            return jsonify(problemDetails), 409



