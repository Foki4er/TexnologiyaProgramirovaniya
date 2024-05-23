from dataclasses import dataclass
from Models.dayofweekname import Dayofweek
from Models.exercisename import Exercise


@dataclass
class DayofweekExercises:
    id: int = None
    Dayofweek: Dayofweek = None
    Exercise: Exercise = None