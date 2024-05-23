from aplication import app
from flask import Response
from flask_restful import Resource
from Services.reportServices import ReportService


_reportService = ReportService()

class ReportController(Resource):
    @staticmethod
    @app.route('/dc/v1/exercise-report.xlsx', methods=['GET'])
    def get_exercise_report():
        report = _reportService.GenerateExerciseReport()
        return Response( report, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                         headers={'Content-Disposition': 'attachment; filename=ExerciseReport.xlsx'},
                         direct_passthrough=True, )