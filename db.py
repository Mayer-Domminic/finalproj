exercise = """
CREATE TABLE exercise (
    exercise_id SERIAL PRIMARY KEY,
    exercise_name VARCHAR(255),
    difficulty_level VARCHAR(255),
    target_muscle_group VARCHAR(255),
    prime_mover_muscle VARCHAR(255),
    secondary_muscle VARCHAR(255),
    tertiary_muscle VARCHAR(255),
    primary_equipment VARCHAR(255),
    primary_items VARCHAR(255),
    secondary_equipment VARCHAR(255),
    secondary_items VARCHAR(255),
    posture VARCHAR(255),
    single_or_double_arm VARCHAR(255),
    continuous_or_alternating_arms VARCHAR(255),
    grip VARCHAR(255),
    load_position_ending VARCHAR(255),
    combination_exercises VARCHAR(255),
    movement_pattern_1 VARCHAR(255),
    movement_pattern_2 VARCHAR(255),
    movement_pattern_3 VARCHAR(255),
    plane_of_motion_1 VARCHAR(255),
    plane_of_motion_2 VARCHAR(255),
    plane_of_motion_3 VARCHAR(255),
    body_region VARCHAR(255),
    mechanics VARCHAR(255),
    laterality VARCHAR(255),
    exercise_classification VARCHAR(255)
);
"""

user = """
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);
"""

workout = """
CREATE TABLE workout (
    workout_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    exercise_details JSONB,  -- Storing exercise IDs with sets and reps as JSON
    description TEXT
);
"""

routine = """
CREATE TABLE routine (
    routine_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    user_id INT REFERENCES users(user_id),
    workout_ids INT[],
    description TEXT
);
"""
# using workout_ids as an array of ids

log = """
CREATE TABLE log (
    log_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    routine_id INT REFERENCES routine(routine_id),
    workout_id INT REFERENCES workout(workout_id),
    date DATE,
    rating TEXT,
    CHECK (routine_id IS NOT NULL OR workout_id IS NOT NULL),
    CHECK (routine_id IS NULL OR workout_id IS NULL)
);
"""

insert_exercise = """
INSERT INTO exercise (
    exercise_name, difficulty_level, target_muscle_group,
    prime_mover_muscle, secondary_muscle, tertiary_muscle,
    primary_equipment, primary_items, secondary_equipment,
    secondary_items, posture, single_or_double_arm,
    continuous_or_alternating_arms, grip, load_position_ending,
    combination_exercises, movement_pattern_1, movement_pattern_2,
    movement_pattern_3, plane_of_motion_1, plane_of_motion_2,
    plane_of_motion_3, body_region, mechanics, laterality,
    exercise_classification
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

import psycopg

def get_connection():
    return psycopg.connect(
        dbname="workout",
        user="postgres",
        password="abc123",
        host="localhost",
        port="5432"
    )

def create_tables(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute(user)
            cursor.execute(routine)
            cursor.execute(exercise)
            cursor.execute(workout)
            cursor.execute(log)
        connection.commit()
        print("created tables")
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
    finally:
        connection.close()

def drop_tables(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS users;")
            cursor.execute("DROP TABLE IF EXISTS routine;")
            cursor.execute("DROP TABLE IF EXISTS exercise;")
            cursor.execute("DROP TABLE IF EXISTS workout;")
            cursor.execute("DROP TABLE IF EXISTS log;")
        connection.commit()
        print("created tables")
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
    finally:
        connection.close()

def add_exercise(connection, exercise):
    with connection.cursor() as cursor:
        cursor.execute(insert_exercise, exercise)
        connection.commit()