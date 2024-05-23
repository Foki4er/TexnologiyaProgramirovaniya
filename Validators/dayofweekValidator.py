import json
from jsonschema import validate

class DayofweekValidator:
    """Класс для проверки json файлов при создании дня недели."""
    def get_schema(self):
        with open('Schemes/dayofweek_schema.json', 'r') as file:
            schema = json.load(file)
        return schema
    
    def validate_dayofweek(self, jsonData):
        schema = self.get_schema()
        validate(instance=jsonData, schema=schema)