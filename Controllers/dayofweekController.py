from flask import jsonify, request, Response
from flask_restful import Resource
from Models.dayofweekname import Dayofweek
from Services.dayofweekServices import DayofweekService
from aplication import app
from Exceptions.dayofweek_not_found_exception import DayofweekNotFoundException
from Exceptions.dayofweek_dublicate_exception import DayofweekDublicateException
from Validators.dayofweekValidator import DayofweekValidator
from jsonschema.exceptions import ValidationError
from Exceptions.problemDetails import ProblemDetails
from logger import service_logger

_dayofweekService = DayofweekService()
_dayofweekValidator = DayofweekValidator()

class dayofweekController(Resource):
    @staticmethod
    @app.route ('/dc/v1/dayofweeks', methods=['GET'])
    def get_dayofweeks():
        return jsonify({"dayofweek": _dayofweekService.findAllDayofweeks()})


    @staticmethod
    @app.route('/dc/v1/dayofweek/<int:id>', methods=['GET'])
    def get_dayofweek(id):
        try:
            dayofweek = _dayofweekService.findDayofweek(id)
            return jsonify(dayofweek)
        except DayofweekNotFoundException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка поиска сущности dayofweekController",
                title=exp.message,
                status=404,
                detail="Запрашиваемый id дня недели не найден",
                instance="http://127.0.0.1:3000/dc/v1/dayofweek"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 404


    @staticmethod
    @app.route('/dc/v1/delete_dayofweek/<int:id>', methods=['DELETE'])
    def delete_dayofweek(id):
        try:
            _dayofweekService.findDayofweek(id)
            _dayofweekService.deleteDayofweek(id)
            return jsonify(id)
        except DayofweekNotFoundException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка поиска сущности dayofweekController",
                title=exp.message,
                status=404,
                detail="Запрашиваемый id дня недели не найден",
                instance="http://127.0.0.1:3000/dc/v1/delete_dayofweek"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 404

    @staticmethod
    @app.route('/dc/v1/add_dayofweek', methods=['POST'])
    def add_dayofweek():
        try:
            request_data = request.get_json()
            _dayofweekValidator.validate_dayofweek(request_data)
            dayofweek = Dayofweek()
            dayofweek.DayofweekName = request_data["DayofweekName"]
            _dayofweekService.addDayofweek(dayofweek)
            return jsonify({"exercises": _dayofweekService.findAllDayofweeks()})

        except ValidationError as err:
            problemDetails = ProblemDetails(
                type="Ошибка валидации в сущности dayofweekController",
                title=err.message,
                status=400,
                detail="Отпрвленный JSON не соответствует схеме.",
                instance="http://127.0.0.1:3000/dc/v1/add_dayofweek"
            )
            res = f"{request_data}\n {err.message}\n {err.schema}"
            service_logger.error(res)
            return jsonify(problemDetails), 400

        except DayofweekDublicateException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка cоздания в сущности dayofweekController",
                title=exp.message,
                status=409,
                detail="Данные отпрвленые в JSON уже есть в БД",
                instance="http://127.0.0.1:3000/dc/v1/add_dayofweek"
            )
            res = f"{request_data}\n {exp.message}"
            service_logger.error(res)
            return jsonify(problemDetails), 409

    @staticmethod
    @app.route('/dc/v1/update_dayofweek/<int:id>', methods=['PUT'])
    def update_dayofweek(id):
        try:
            _dayofweekService.findDayofweek(id)

            request_data = request.get_json()
            _dayofweekValidator.validate_dayofweek(request_data)

            dayofweek = Dayofweek()
            dayofweek.DayofweekName = request_data["DayofweekName"]

            _dayofweekService.updateDayofweek(id, dayofweek)
            return jsonify({"dayofweeks": _dayofweekService.findAllDayofweeks()})

        except ValidationError as err:
            problemDetails = ProblemDetails(
                type="Ошибка валидации в сущности dayofweekController",
                title=err.message,
                status=400,
                detail="Отпрвленный JSON не соответствует схеме.",
                instance="http://127.0.0.1:3000/dc/v1/update_dayofweek"
            )
            res = f"{request_data}\n {err.message}\n {err.schema}"
            service_logger.error(res)
            return jsonify(problemDetails), 400

        except DayofweekNotFoundException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка поиска сущности dayofweekController",
                title=exp.message,
                status=404,
                detail="Запрашиваемый id дня недели не найден",
                instance="http://127.0.0.1:3000/dc/v1/update_dayofweek"
            )
            service_logger.error(exp.message)
            return jsonify(problemDetails), 404

        except DayofweekDublicateException as exp:
            problemDetails = ProblemDetails(
                type="Ошибка обновления в сущности dayofweekController",
                title=exp.message,
                status=409,
                detail="Данные отпрвленые в JSON уже есть в БД",
                instance="http://127.0.0.1:3000/dc/v1/update_dayofweek"
            )
            res = f"{request_data}\n {exp.message}"
            service_logger.error(res)
            return jsonify(problemDetails), 409
