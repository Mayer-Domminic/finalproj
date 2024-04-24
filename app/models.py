class Workout:
    def __init__(self, db, workout_id=None, date=None, duration=None, type=None):
        self.db = db
        self.workout_id = workout_id
        self.date = date
        self.duration = duration
        self.type = type

    def save(self):
        with self.db.cursor() as cur:
            if self.workout_id is None:
                pass
            else:
                pass