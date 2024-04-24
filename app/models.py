class User:
    def __init__(self, db, user_id=None, username=None, email=None, password_hash=None, created_at=None, last_login=None):
        self.db = db
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.last_login = last_login

    def save(self):
        with self.db.cursor() as cur:
            if self.user_id is None:
                cur.execute(
                    "INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING user_id",
                    (self.username, self.email, self.password_hash)
                )
                self.user_id = cur.fetchone()[0]
            else:
                cur.execute(
                    "UPDATE Users SET username=%s, email=%s, password_hash=%s, last_login=%s WHERE user_id=%s",
                    (self.username, self.email, self.password_hash, self.last_login, self.user_id)
                )
            self.db.commit()

    def delete(self):
        with self.db.cursor() as cur:
            cur.execute("DELETE FROM Users WHERE user_id=%s", (self.user_id,))
            self.db.commit()


class Workout:
    def __init__(self, db, workout_id=None, user_id=None, date=None, duration=None, type=None):
        self.db = db
        self.workout_id = workout_id
        self.user_id = user_id
        self.date = date
        self.duration = duration
        self.type = type

    def save(self):
        with self.db.cursor() as cur:
            if self.workout_id is None:
                cur.execute(
                    "INSERT INTO Workouts (user_id, date, duration, type) VALUES (%s, %s, %s, %s) RETURNING workout_id",
                    (self.user_id, self.date, self.duration, self.type)
                )
                self.workout_id = cur.fetchone()[0]
            else:
                cur.execute(
                    "UPDATE Workouts SET date=%s, duration=%s, type=%s WHERE workout_id=%s",
                    (self.date, self.duration, self.type, self.workout_id)
                )
            self.db.commit()

    def delete(self):
        with self.db.cursor() as cur:
            cur.execute("DELETE FROM Workouts WHERE workout_id=%s", (self.workout_id,))
            self.db.commit()


class Exercise:
    def __init__(self, db, exercise_id=None, name=None, description=None, type=None):
        self.db = db
        self.exercise_id = exercise_id
        self.name = name
        self.description = description
        self.type = type

    def save(self):
        with self.db.cursor() as cur:
            if self.exercise_id is None:
                cur.execute(
                    "INSERT INTO Exercises (name, description, type) VALUES (%s, %s, %s) RETURNING exercise_id",
                    (self.name, self.description, self.type)
                )
                self.exercise_id = cur.fetchone()[0]
            else:
                cur.execute(
                    "UPDATE Exercises SET name=%s, description=%s, type=%s WHERE exercise_id=%s",
                    (self.name, self.description, self.type, self.exercise_id)
                )
            self.db.commit()

    def delete(self):
        with self.db.cursor() as cur:
            cur.execute("DELETE FROM Exercises WHERE exercise_id=%s", (self.exercise_id,))
            self.db.commit()


class Routine:
    def __init__(self, db, routine_id=None, user_id=None, name=None, description=None, type=None, created_at=None):
        self.db = db
        self.routine_id = routine_id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.type = type
        self.created_at = created_at

    def save(self):
        with self.db.cursor() as cur:
            if self.routine_id is None:
                cur.execute(
                    "INSERT INTO Routines (user_id, name, description, type) VALUES (%s, %s, %s, %s) RETURNING routine_id",
                    (self.user_id, self.name, self.description, self.type)
                )
                self.routine_id = cur.fetchone()[0]
            else:
                cur.execute(
                    "UPDATE Routines SET name=%s, description=%s, type=%s WHERE routine_id=%s",
                    (self.name, self.description, self.type, self.routine_id)
                )
            self.db.commit()

    def delete(self):
        with self.db.cursor() as cur:
            cur.execute("DELETE FROM Routines WHERE routine_id=%s", (self.routine_id,))
            self.db.commit()

