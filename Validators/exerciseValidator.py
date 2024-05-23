import json
from jsonschema import validate

class ExerciseValidator:
    """Класс для проверки json файлов при создании занятия."""
    def get_schema(self):
        with open('Schemes/exercise_schema.json', 'r') as file:
            schema = json.load(file)
        return schema
    
    def validate_exercise(self, jsonData):
        schema = self.get_schema()
        validate(instance=jsonData, schema=schema)