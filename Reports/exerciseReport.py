import io
from flask import request
from xlsxwriter import Workbook
from werkzeug.wsgi import wrap_file


class ExerciseReport:
    def buid(exercises):
        file = io.BytesIO()
        wb = Workbook(file)
        ws = wb.add_worksheet()
        row = 0
        for exercise in exercises:
            column = 0
            for _key, _value in exercise.items():
                ws.write(row, column, _value)
                column += 1
            row += 1
        wb.close()
        file.seek(0)
        wrapped_file = wrap_file(request.environ, file)
        return wrapped_file

